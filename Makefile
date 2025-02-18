build:
	docker-compose build

build-nc:
	docker-compose build --no-cache

down:
	docker-compose down --volumes

run:
	make down && docker-compose up -d

stop:
	docker-compose stop

convert-base:
	docker exec executor python json_to_csv_converter.py --source-dir "$(source-dir)" --target-dir "$(target-dir)" --filenames "$(filenames)"

convert:
	make run && sleep 5 && make convert-base source-dir=/opt/yelp_dataset target-dir=/opt/yelp_dataset filenames=yelp_academic_dataset_business,yelp_academic_dataset_checkin,yelp_academic_dataset_review,yelp_academic_dataset_tip,yelp_academic_dataset_user && make down

upload-base:
	docker exec executor python csv_uploader.py --source-dir "$(source-dir)" --gcs-bucket "$(gcs-bucket)" --filenames "$(filenames)" --workers 1

upload:
	make run && sleep 5 && make upload-base source-dir=/opt/yelp_dataset gcs-bucket=dana-quality-test filenames=USW00093084_SAFFORD_MUNICIPAL_AP_precipitation_inch,USW00093084_temperature_degreeF,yelp_academic_dataset_business,yelp_academic_dataset_checkin,yelp_academic_dataset_review,yelp_academic_dataset_tip,yelp_academic_dataset_user && make down

generate-base:
	docker exec executor python external_table_generator.py --filenames "$(filenames)" --gcs-bucket "$(gcs-bucket)" --project-name "$(project-name)" --dataset-name "$(dataset-name)"

generate:
	make run && sleep 5 && make generate-base filenames=USW00093084_SAFFORD_MUNICIPAL_AP_precipitation_inch,USW00093084_temperature_degreeF,yelp_academic_dataset_business,yelp_academic_dataset_checkin,yelp_academic_dataset_review,yelp_academic_dataset_tip,yelp_academic_dataset_user gcs-bucket=dana-quality-test project-name=dana-quality-test dataset-name=dana_quality_test && make down
