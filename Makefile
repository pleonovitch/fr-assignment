init_config:
		j2 --format=yaml deployment/deployment.j2 config.yaml -o deployment/deployment.yaml
		j2 --format=yaml tf/terraform.tfvars.j2 config.yaml -o tf/terraform.tfvars

support_image: init_config
		echo "Preparing Support image"
		cd support_images; gcloud builds submit --config cloudbuild.yaml .
app_image: support_image
		echo "Preparing application image"
		cd app; gcloud builds submit --config cloudbuild.yaml . 

tf: init_config
		cd tf; terraform init
		terraform apply -auto-approve
		gcloud container clusters get-credentials $(terraform output kubernetes_cluster_name) --region $(terraform output region)

clean:
		cd tf; terrform destroy -auto-approve

deploy_app: app_image tf
		#deploy
		kubectl apply -f deployment/deployment.yaml 
		kubectl apply -f deployment/service.yaml
		#obtain IP of service
		$(eval SERVICE_IP := $(shell deployment/wait_for_ip.sh))
		echo $(SERVICE_IP)
		#store expected value of TOTAL_LEN element of response payload
		$(eval EXPECTED_TEST_TL:= $(shell cat test_data/expected_TOTAL_LEN))
		echo $(EXPECTED_TEST_TL)
		#obtain runtime value of TOTAL_LEN element of response payload
		$(eval TEST_TL := $(shell curl -s -F file=@test_data/test.txt  $(SERVICE_IP)/process | jq ".response.TOTAL_LEN"))
		echo $(TEST_TL)
		#compare expected versus runtime
		deployment/fail_if_not_equal.sh $(EXPECTED_TEST_TL) $(TEST_TL)
		@echo "Deployed and validated"



