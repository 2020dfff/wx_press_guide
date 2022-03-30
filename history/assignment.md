# Twitter(推特)的安全机制认证与加密流程分析：

> 费扬 519021910917
>
> 《现代密码学》课程设计大作业

![img](https://raw.githubusercontent.com/2020dfff/md_fig/master/data/01foKG6vvE36lR79PKych6X-2.fit_lim.size_768x432.v1594911840-16480299171061.jpg)

[toc]

## 推特的安全问题背景：		

​		[Twitter推特](https://twitter.com)允许用户与世界上的任何人联系，但它也已经成为一个充满骚扰和虐待的危险场所。人们一直是协调骚扰活动的目标，这些活动可能涉及从威胁和垃圾邮件到帐户黑客攻击甚至更糟的任何事情。Twitter因行动不够快而从其平台上删除骚扰者而受到批评，并且在许多情况下，允许滥用的行为十分猖獗。

​		最近几个月，Twitter已经开始测试许多新功能，以改变人们在平台上互动的方式。有些，比如阻止人们分享[他们没有读过的文章](https://www.pcmag.com/news/twitter-to-ask-did-you-actually-read-this-article-before-retweets)，可能会有所帮助。当谈到在Twitter上保持安全时，重要的是要注意社交媒体公司在冲突中能得到茁壮成长。虽然有一些方法可以保护您的帐户，但您无法完全保护自己免受各种形式的滥用。

​		在2020年七月，对[Twitter最受瞩目的用户的](https://www.pcmag.com/news/huge-twitter-hack-hits-accounts-of-elon-musk-bill-gates-obama-more)黑客攻击来自推特内部：Twitter黑客攻击了马斯克，比尔·盖茨，奥巴马等名人的账户。黑客接管了这些账户，以鼓励公众将比特币捐赠给一个数字钱包，该钱包已经收集了超过11万美元的资金。诈骗者声称："我们已经与Crypto For Health合作，并向社区返还了5000 BTC。向钱包发送资金的人被承诺他们将获得双倍的退款”。为了解决这个问题，经过验证的用户的推文功能短暂关闭。Twitter后来称其为"coordinated social engineering attack"。

![img](https://raw.githubusercontent.com/2020dfff/md_fig/master/data/06yAoFzrUmfo1urhPmBP1oq-1.fit_lim.v1594850479.jpg)

​		因此，在推特上保护自己的唯一有保证的方法是在社交媒体上少花时间或者干脆[删除您的帐户](https://www.pcmag.com/how-to/how-to-delete-twitter-and-your-terrible-tweets)。为了留住更多的用户，Twitter采取了以下的方法，使用户尽可能安全。

## 推特身份验证登录：

Twitter API 处理大量数据。我们确保开发人员和用户都保护此数据的方式是通过身份验证。有几种身份验证方法，下面列出了每种方法。

- **OAuth 1.0a 用户上下文**

  OAuth 1.0a 允许授权的 Twitter 开发者应用访问私人帐户信息或代表 Twitter 帐户执行 Twitter 操作。

  [参考链接](https://developer.twitter.com/en/docs/authentication/oauth-1-0a)

- **基本身份验证**

  Twitter 的许多企业 API 都需要使用 HTTP 基本身份验证。

  [参考链接](https://developer.twitter.com/en/docs/authentication/basic-auth)

- **OAuth 2.0 持有者令牌**

  OAuth 2.0 持有者令牌允许 Twitter 开发人员应用访问 Twitter 上公开提供的信息。

  [参考链接](https://developer.twitter.com/en/docs/authentication/oauth-2-0)

- **使用 PKCE 的 OAuth 2.0 授权代码流**

  OAuth 2.0 用户上下文允许您代表另一个帐户进行身份验证，从而更好地控制应用程序的范围，并且授权跨多个设备流动。

  [参考链接](https://developer.twitter.com/en/docs/authentication/oauth-2-0/user-context)

​	这里我们以第一种方法，即OAuth 1.0a为例，演示如何获取用户的访问令牌：

### OAuth 1.0a：

​		要代表其他用户提出请求，您首先需要获得该用户的授权。 这是通过 3-legged OAuth 流程实现的，在此期间您重定向用户以授权您的应用程序并接收用户的访问令牌和秘密作为交换。

​		请注意，用户访问令牌是为每个开发者应用程序唯一生成的； 换句话说，如果你为 App A 生成了一个 Access Token，那么这个特定的 Access Token 对 App B 就不起作用了。

​		3-legged OAuth 流程（有时也称为“使用 Twitter 登录”）通常涉及三方：

1. 最终用户或资源所有者：这里指您要代表其发出 API 请求的 Twitter 用户。
2. 客户端或第三方应用程序：这里指您的 Twitter 开发者应用程序。
3. 服务器或授权服务器：这里指推特。











​	





