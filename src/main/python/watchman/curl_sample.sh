set -x
ACCOUNT_ID=2115113
NRQL="SELECT count(appName) FROM PageView"

curl -s -H "Accept: application/json" \
-H "X-Query-Key: $NEW_RELIC_INSIGHT_API_KEY" \
--data-urlencode "nrql=$NRQL" \
"https://insights-api.newrelic.com/v1/accounts/$ACCOUNT_ID/query"

set +x