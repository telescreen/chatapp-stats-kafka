```sql
CREATE STREAM CHAT_MESSAGES_STREAM (
    username VARCHAR,
    message_content VARCHAR,
    message_time VARCHAR
) WITH (
    KAFKA_TOPIC='chat_users',
    VALUE_FORMAT='json',
    timestamp='message_time',
    timestamp_format='dd-MM-yyyy HH:mm:ss'
);
```

```sql
CREATE TABLE COUNT_USERS_TABLE AS
    SELECT USERNAME, count(*) AS NUMBER_OF_MESSAGES
    FROM CHAT_MESSAGES_STREAM
    GROUP BY USERNAME
    EMIT CHANGES;
```

```sql
CREATE STREAM CHAT_MESSAGES_STREAM_NOTS (
    username VARCHAR,
    message_content VARCHAR
) WITH (
    KAFKA_TOPIC='chat_users',
    VALUE_FORMAT='json'
);
```

```sql
CREATE SINK CONNECTOR SINK_ELASTIC WITH (
    'connector.class' = 'io.confluent.connect.elasticsearch.ElasticsearchSinkConnector',
    'topics' = 'CHAT_MESSAGE_AVRO',
    -- 'key.converter' = 'org.apache.kafka.connect.storage.StringConverter',
    -- 'value.converter' = 'org.apache.kafka.connect.json.JsonConverter',
    -- 'value.converter.schemas.enable' = 'false',
    'connection.url' = 'http://elasticsearch:9200',
    'type.name' = '_doc',
    'key.ignore' = 'true',
    'schema.ignore'  = 'true'
);
```

```sql
CREATE STREAM CHAT_MESSAGE_AVRO
WITH (VALUE_FORMAT='AVRO') AS SELECT * FROM CHAT_MESSAGES_STREAM;
```