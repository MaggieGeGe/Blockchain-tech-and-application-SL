
# ETH以太坊

1 bitcoin时间太长 10min ETH缩短为十几秒
2 mining puzzle：对内存要求高，限制了asic芯片的使用
3 权益证明代替工作量证明
4 smart contract：去中心化合约的支持

# 账户

account-based ledger
存在账户余额，不记录源头。还记录交易次数。

ETH中存在两类账户：
- externally owned account
  - BALANCE
  - NONCE:记录交易次数
- smart contract account
  - nonce：记录被合约调用的次数
  - code
  - storage
合约账户不能主动发交易，只能由外部账户发起
创建合约的时候存在地址，调用的时候用地址。调用时代码不变存储变。

BTC匿名性。
ETH支持智能合约，要求参与者有稳定的身份。

# 状态树

账户地址到账户状态的映射。

trie: retrieval 
merkle 

address: 40个16进制 o～f