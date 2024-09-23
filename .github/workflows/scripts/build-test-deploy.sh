#!/bin/bash

set -e
set -x

export DOCKER_BUILDKIT=1 # activate for all future commands in the current shell

REPOSITORY=${REPOSITORY:-bikes}
IMAGE_TAG=${IMAGE_TAG:-latest}

# PLATFORM=linux/amd64,linux/arm64
PLATFORM=linux/arm64
# PLATFORM=${PLATFORM:-linux/amd64}

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo "pwd=$PWD script_dir=${SCRIPT_DIR}"

export PRODUCTION=true

#if [ "$1" == "test" ]; then
    # docker compose build flannelcat-webapi --quiet
    # docker compose run --entrypoint ruff flannelcat-webapi check .
    # docker compose run --entrypoint mypy flannelcat-webapi .
    # docker compose run --entrypoint bash flannelcat-webapi -c "coverage run --source='.' manage.py test --keepdb && coverage report && coverage xml -o ./test-results/coverage.xml"
#fi

if [ "$1" = "deploy" ]; then
  docker buildx build \
      --tag "${REPOSITORY}:${IMAGE_TAG}" \
      --platform "${PLATFORM}" \
      --load \
      "${SCRIPT_DIR}/../../../src/"

  docker tag "${REPOSITORY}:${IMAGE_TAG}" "$REGISTRY/${REPOSITORY}:${IMAGE_TAG}"
  docker push "$REGISTRY/${REPOSITORY}:${IMAGE_TAG}"
fi

if [ "$1" = "deploy" ] || [ "$1" = "update" ]; then
  FULL_IMAGE="408799413549.dkr.ecr.us-west-2.amazonaws.com/${REPOSITORY}:${IMAGE_TAG}"
  TASK_DEFINITION=$(aws ecs describe-task-definition --task-definition "$TASK_FAMILY" --region "$AWS_REGION")
  NEW_TASK_DEFINITION=$(echo "$TASK_DEFINITION" | jq --arg IMAGE "$FULL_IMAGE" '.taskDefinition | .containerDefinitions[0].image = $IMAGE | del(.taskDefinitionArn) | del(.revision) | del(.status) | del(.requiresAttributes) | del(.compatibilities) |  del(.registeredAt)  | del(.registeredBy)')
  NEW_TASK_INFO=$(aws ecs register-task-definition --region "$AWS_REGION" --cli-input-json "$NEW_TASK_DEFINITION")
  NEW_REVISION=$(echo "$NEW_TASK_INFO" | jq '.taskDefinition.revision')
  aws ecs update-service --cluster "${ECS_CLUSTER}" --service "${SERVICE_NAME}" --task-definition "${TASK_FAMILY}:${NEW_REVISION}"

  aws ssm put-parameter \
      --name "/${ENV}/service/${SERVICE_NAME}/ecr-image-tag" \
      --value "${IMAGE_TAG}" \
      --type String \
      --overwrite
fi