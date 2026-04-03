.PHONY: help setup test reset destroy ssh-web ssh-db ssh-comms

help: ## Show available commands
	@echo ""
	@echo "  STARFALL DEFENCE CORPS — Gateway Simulation"
	@echo "  Operation: First Contact"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
	@echo ""

setup: ## Launch the forward observation post (3 nodes)
	@bash scripts/setup-lab.sh

test: ## Run ARIA assessment verification
	@bash scripts/check-work.sh

reset: ## Destroy and rebuild all nodes
	@bash scripts/reset-lab.sh

destroy: ## Tear down everything (containers, keys, venv)
	@bash scripts/destroy-lab.sh

ssh-web: ## SSH into sdc-fwd-web (Ubuntu, port 2231)
	@ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
		-i .docker/ssh-keys/cadet_key cadet@localhost -p 2231

ssh-db: ## SSH into sdc-fwd-db (Rocky Linux, port 2232)
	@ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
		-i .docker/ssh-keys/cadet_key cadet@localhost -p 2232

ssh-comms: ## SSH into sdc-fwd-comms (Ubuntu, port 2233)
	@ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
		-i .docker/ssh-keys/cadet_key cadet@localhost -p 2233
