

partner_reccom = df.pivot_table(index='user_id',columns='key_word',values='weight').fillna(0)