FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY ./docker/prod/nginx/orwell_shop.conf /etc/nginx/conf.d/
COPY ./cert_files/secure_s79_ierg4210_ie_cuhk_edu_hk.key /etc/nginx/conf.d/
COPY ./cert_files/secure_s79_ierg4210_ie_cuhk_edu_hk.chained.crt /etc/nginx/conf.d/


EXPOSE 80
EXPOSE 443