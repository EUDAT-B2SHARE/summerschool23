FROM elasticsearch:2.4.6
EXPOSE 9200 9300

RUN cd /usr/share/elasticsearch && \
    ./bin/plugin install -b mapper-attachments

CMD ["elasticsearch"]
