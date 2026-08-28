
## Firma Unvanı Gösterimi Kararı

Ürün listesinde `company_id` yerine (ya da yanında) firma unvanını göstermek için üç yöntem
değerlendirildi:

- **(a) Her istekte firma servisine sor:** Veri her zaman güncel olur, ama ciddi bir maliyeti
  var. Sayfa boyutu 20 olduğu için, bir liste isteği 20 ayrı HTTP çağrısı yapar (N+1 sorgu
  problemi). Üstüne, firma servisi çökerse ürün listesi de çöker — bağımlılık riski yaratır.

- **(b) Unvanı products tablosuna kopyala:** Ürün oluşturulurken firma unvanı da kaydedilir.
  Hızlı ve bağımsız çalışır, firma servisine her seferinde sormaya gerek kalmaz.

- **(c) Hiç gösterme, arayüz birleştirsin:** Servisler temiz kalır ama sorunu çözmez, sadece
  frontend'e devreder.

**Seçilen yöntem: (b)**

(a) seçeneği, küçük bir kolaylık (unvanın her zaman güncel olması) için ağır bir bedel
(N+1 sorgu, firma servisine bağımlılık) getiriyor. (c) seçeneği teknik olarak temiz ama
sorunu çözmüyor, sadece taşıyor. (b) seçeneği ise firma unvanının **sık değişmeyen** bir
alan olması sayesinde makul bir takas sunuyor: unvan değişmediği sürece hiçbir sorun
yaratmaz, değiştiği nadir durumda ise elle güncellemek büyük bir maliyet değildir.

**Bilinen bedel:** Firma unvanı `firma-servisi`'nde değiştirildiğinde, bu değişiklik
`urun-servisi`'ndeki kopyaya otomatik yansımaz — iki veritabanı arasında bir senkronizasyon
mekanizması olmadığı için. Bu bilinçli olarak kabul edilen bir bedel; gerçek bir sistemde bu,
olay tabanlı (event-driven) bir mimari ile çözülür.



## Dokümana Önerdiğim Eklemeler

Standartlar dokümanının 3.3 bölümünde karşılığı olmayan, bu hafta karşılaştığım üç durum kodu için öneriler:

- **204 No Content:** Bir kaynak başarıyla silindiğinde, dönecek bir gövde olmadığını belirtmek için kullanılmalı (örn. `DELETE /api/v1/products/{id}`).
- **503 Service Unavailable:** İstek ve kodumuz doğru olduğu hâlde, bağımlı olunan başka bir servise ulaşılamadığında veya zaman aşımına uğradığında kullanılmalı — bu bizim değil, bağımlı servisin geçici arızasıdır.
- **401 Unauthorized:** İsteğin kimlik bilgisi (bu projede `X-User-Id` başlığı) eksik veya geçersiz olduğunda kullanılmalı; sunucu isteği yapanın kim olduğunu bilmiyor demektir.