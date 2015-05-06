import recommendations
import deliciousrec

delicious_users = deliciousrec.initUserDict('Python', 10)
delicious_users = deliciousrec.fillItems(delicious_users)

test_user = delicious_users.keys()[0]

print recommendations.top_matches(delicious_users, test_user)
print recommendations.get_recommendatios(delicious_users, test_user)[0:4]