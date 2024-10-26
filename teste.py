import psycopg2
from dbbase.md import mod

total = len(mod)
x=0
for i in mod:
    tabela=f"dbbase_{i.lower()}"
    # Configurações de conexão
    conn = psycopg2.connect(
        dbname='verceldb',
        user='default',
        password='2VJpPEtb8QBI',
        host='ep-sparkling-tree-689152.us-east-1.aws.neon.tech',
        port='5432'
    )

    # Criar um cursor
    cur = conn.cursor()

    # Ler os dados da tabela de origem
    try:
        cur.execute(f"SELECT * FROM {tabela}")
    except:
        continue
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    # Fechar a conexão com a tabela de origem
    cur.close()
    conn.close()

    # Agora, conectar ao banco de dados de destino
    conn_destino = psycopg2.connect(
        dbname='tbre',
        user='Django',
        password='tuTGMFhERpC%Y|xJ',
        host='35.198.50.92',
        port='5432'
    )

    # Criar um novo cursor para a tabela de destino
    cur_destino = conn_destino.cursor()

    # Inserir os dados na tabela de destino
    its=len(rows)
    y=0
    for row in rows:
        try:
            insert_query = f"INSERT INTO {tabela} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(row))})"
        except:
            break
        cur_destino.execute(insert_query, row)
        y+=1
        print(f"itens {y} de {its}, {(y / its)*100}%")
    # Confirmar as alterações e fechar a conexão
    conn_destino.commit()
    cur_destino.close()
    conn_destino.close()
    x+=1
    print(f"models {x} de {total}, {x/total}%    {i}")
