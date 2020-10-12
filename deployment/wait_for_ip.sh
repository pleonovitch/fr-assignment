#!/bin/sh
# todo: add max attempt contrain to fail after certain number of attempts
external_ip=""
while [ -z $external_ip ]; do
    #sleep 10
    external_ip=$(kubectl get service wordcrunch --template="{{range .status.loadBalancer.ingress}}{{.ip}}{{end}}")
done
echo $external_ip