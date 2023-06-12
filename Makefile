PYTHON=python3

.PHONY: help clean tar format report

help:	    ## Show this help message
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

clean:	    ## Clean the directory
	git clean -dxf -e venv/ -e mlruns/ -e .idea/ -e db

tar:	    ## Tar the current project
	tar --exclude="./.git" --exclude="./__pycache" -czvf project.tar .

format:	    ## Format python files in place with black formatter
	black -l 120 .

mlflow:     ## See Neural Net results via MLflow
	mlflow ui

static:     ## Lint
	pylint --disable=C0103,C0301,R1711,R1705,R0903,R1734,W1514,C0411,R0913,R0902,R0914,R1735 .

sonarqube:  ## Run sonarqube analysis (local instance)
	sonar-scanner -Dsonar.projectKey=march-madness -Dsonar.sources=. -Dsonar.host.url=http://localhost:9000 -Dsonar.token=sqp_03f9f4ad6fdd9892f8331f9a52ea28457edbe85f
