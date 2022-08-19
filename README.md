# RP2040-Dof9-Lcd-Ble-Battery-Micropython
本程式由Micropython編寫，主要是9軸感測器訊號處理與LCD顯示及藍芽傳輸之功能。

## 模組堆疊方案
堆疊的層順序除了頂層LCD模組外其他模組並沒有特別順序要求,按照正確插Pin的方向的去疊起來就可以了!

![全部模組](/images/AllModelView.png)

### RP2040開發模組
我使用的是[升級版](https://www.waveshare.net/shop/RP2040-Plus.htm),當然也可以使用[初版品](https://www.waveshare.net/shop/Raspberry-Pi-Pico.htm)就是了。

### LCD模組
我用的LCD模組似乎停產了!所以建議使用[後繼品](https://www.waveshare.net/shop/Pico-LCD-1.14.htm);但不管是圖中的產品或後繼品也會遇與其他模組衝突的狀況而導致按鈕無法全部都使用的問題,目前只能使用GP17腳位上的按鈕(圖中的key1鍵或後繼品中的B鍵)。

### Dof9模組
這個模組挺尷尬的,因為ICM20948的晶片才是MPU9250晶片的後繼品,但因為晶片生產商供貨問題目前微雪官網只能買到[MPU9250版的模組](https://www.waveshare.net/shop/Pico-10DOF-IMU.htm),卻買不到我用的這個模組。似乎ICM20948與MPU9250有所不同所以Library無法直接套用,這部分還需要嘗試一下;但因為我手邊倒是沒有MPU9250版的模組所以暫時無法確認。另一方面因為ICM20948工作電壓比MPU9250低,所以模組佈局上MPU9250少了電壓轉換的布局所以相對精簡許多。

### Battery模組
在微雪官網上它叫[UPS系統(電容量600mah)](https://www.waveshare.net/shop/Pico-UPS-B.htm),其實可以不需要這層模組,因為RP2040升級版已經自帶一個電池插座,挑選能符合的插座與能塞進兩個模組之間層縫的大小就可以了，但如果使用RP2040初版品做開發就需要這個電池模組了，而這麼電池模組其實具有讀取電量功能的,只是這部分程式我尚未實現。
