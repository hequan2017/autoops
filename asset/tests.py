a = [('***************************', 1, '.row', '***************************'), '\n', ('           ID', ':', 1), '\n', ('        stage', ':', 'RERUN'), '\n', ('     errlevel', ':', 0), '\n', ('  stagestatus', ':', 'Execute Successfully'), '\n', (' errormessage', ':', 'None'), '\n', ('          SQL', ':', 'use hequan'), '\n', ('Affected_rows', ':', 0), '\n', ('     sequence', ':', "'1513842575_123_0'"), '\n', ('backup_dbname', ':', 'None'), '\n', (' execute_time', ':', '0.000'), '\n', ('      sqlsha1', ':', ''), '\n', ('***************************', 2, '.row', '***************************'), '\n', ('           ID', ':', 2), '\n', ('        stage', ':', 'NONE'), '\n', ('     errlevel', ':', 2), '\n', ('  stagestatus', ':', 'None'), '\n', (' errormessage', ':', "Access denied for user '123456'@'192.168.10.83' (using password: YES)"), '\n', ('          SQL', ':', 'Global environment'), '\n', ('Affected_rows', ':', 0), '\n', ('     sequence', ':', 'None'), '\n', ('backup_dbname', ':', 'None'), '\n', (' execute_time', ':', '0'), '\n', ('      sqlsha1', ':', 'None'), '\n']

b =('***************************', 1, '.row', '***************************')


print(type(b))
print(b)

c = []

for i in b:
    c.append(i)

print(c)