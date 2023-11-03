FROM nginx:latest
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/

#FOR PROD
# COPY ./ssl /etc/nginx/ssl/
# RUN openssl dhparam -out /etc/nginx/dhparam.pem 2048
