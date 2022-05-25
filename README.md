# python-tronlink-scan
波场链的扫块功能

安装需要的用到的插件  
```
pip install -r requirements.txt
```
运行即可,有需要的可调整为数据库的结构来存  
```
python main.py
```

example:    
需要记录的合约 config/contract.csv  
地址|名称|精度 
```
address,name,decimals
TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t,USDT,6
TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8,USDC,6
TAFjULxiVgT4qWk6UZwjqwZXTSaGaqnVp4,BitTorrent,18
```  
需要记录的钱包 config/wallet.csv  
地址|密钥 
```
address,private_key
TSRg164MqUKMxDn2eQYvAg9iFNhQYXAFa8,
TNV2h4c2ibuQKes5XTgwuuP9mdfQiAHxpL,
TGn37A4yEjVBCXojhFNpZvovWvfNdzwC3x,
```  
激活的要以 config/transaction.csv  
hash|区块|发出地址|接收地址|区块时间|数额|合约地址|状态   
```
hash,block,from,to,block_at,amount,contract_address,status
f474e2ceb883637aae1f666adc7714309bf933cfd956173c68bd0512e2190f34,40967609,TPJA5T1QaJEZnCgujC36GpX2wGLYsYnqAh,TNV2h4c2ibuQKes5XTgwuuP9mdfQiAHxpL,2022-05-25 13:32:27,28.29,TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t,success
fbd03d69af7ba8e1f7c56dd11738c8d6269497193daf0efa23eff3ed477e6f12,40969058,TJDFLrCiKneK2rXjCudn4gGMcYhVeqB8ru,TGn37A4yEjVBCXojhFNpZvovWvfNdzwC3x,2022-05-25 14:45:06,7229.02,TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t,success
```