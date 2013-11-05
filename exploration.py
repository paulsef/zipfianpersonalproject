import etl
import pandas as pd
df = etl.main('jsonout/0.json')
df.append(etl.main('jsonout/5000.json'))
df.append(etl.main('jsonout/10000.json'))
df.append(etl.main('jsonout/15000.json'))

df['regiseted'] = pd.to_datetime(df['regiseted'])