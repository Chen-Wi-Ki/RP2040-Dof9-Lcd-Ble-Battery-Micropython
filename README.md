# RP2040-Dof9-Lcd-Ble-Battery-Micropython
本程式由Micropython編寫，主要是9軸感測器訊號處理與LCD顯示及藍芽傳輸之功能。Micropython編寫前需要先掛入[UF2](http://www.micropython.org/download/rp2-pico/)文件，這是它們特有的一種bootloader方法，另外我的編成環境是[Thonny IDE](https://thonny.org/)，基礎教學網路上都找得到本專案就不另外贅述了。

## 模組堆疊方案
堆疊的層順序除了頂層LCD模組外其他模組並沒有特別順序要求,按照正確插Pin的方向去疊起來就可以了,另外LCD上3顆按鈕會被其他模組的功能佔用導致它們實際上是無作用的。

![全部模組](/images/AllModelView.png)

### RP2040開發模組
我使用的是[升級版](https://www.waveshare.net/shop/RP2040-Plus.htm),當然也可以使用[初版品](https://www.waveshare.net/shop/Raspberry-Pi-Pico.htm)製作。

### LCD模組
我用的LCD模組似乎停產了!所以建議使用[後繼品](https://www.waveshare.net/shop/Pico-LCD-1.14.htm);但不管是圖中的產品或後繼品也會與其他模組衝突而導致按鈕無法全部都使用的問題,目前只能使用GP17腳位上的按鈕(圖中的key1鍵或後繼品中的B鍵)。

### Dof9+1模組(3軸加速計+3軸陀螺儀+3軸磁力計+1大氣壓計)
這個模組挺尷尬的,因為ICM20948的晶片才是MPU9250晶片的後繼品,但晶片生產商供貨不及，目前微雪官網只能買到[MPU9250版的模組](https://www.waveshare.net/shop/Pico-10DOF-IMU.htm),卻買不到我用的這個模組。似乎ICM20948與MPU9250配置上有所不同所以Library無法直接套用,這部分還需要嘗試一下,無奈因為我手邊沒有MPU9250版的模組所以暫時無法確認。另一方面因為ICM20948工作電壓比MPU9250低,所以模組佈局上MPU9250少了電壓轉換的關係所以相對精簡許多。

### BLE模組
這個其實是[雙模(BLE+SPP)藍芽模組](https://www.waveshare.net/shop/Pico-BLE.htm)來著，而它佔用了1個LCD的按鈕腳位(GP15)所以Key0(A鍵)無法作用。

### Battery模組
在微雪官網上它叫[UPS系統(電容量600mah)](https://www.waveshare.net/shop/Pico-UPS-B.htm),其實可以不需要這層模組,因為RP2040升級版有自帶一個電池插座,挑選符合的插座與能塞進兩個模組之間層縫的電池大小就可以了;但如果使用RP2040初版品做開發就需要這個電池模組了,而這個電池模組其實具有讀取電量的功能只是這部分程式我尚未實現。
