# 密码学原理

密码学中的[哈希函数](https://zh.wikipedia.org/wiki/%E6%95%A3%E5%88%97%E5%87%BD%E6%95%B8) Cryptographic hash function
### 性质1：collision resistance/free

x \ne y , H(x)=H(y)
 
理论上无法证明。

### 性质2 ：hiding

空间足够大，暴力遍历不可行。分布均匀。

### `Bitcoin`专有性质3：puzzle friendly

计算是不可预测的，只能一个一个尝试。挖矿的过程是找一个随机数nonce，和其他信息结合一起获得哈希值。
满足`H(block header)<=target`

