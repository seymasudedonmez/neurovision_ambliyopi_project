import json
import os
from datetime import datetime, timedelta

class DataManager:
    def __init__(self, db_file="forest_guardian_data.json"):
        self.db_file = db_file
        self.lock_file = "data/lock_data.json"
        self.weekly_file = "data/weekly_tracking.json"
        
        os.makedirs("data", exist_ok=True)
        
        self.library_source = {

            1: {"title": "1. Okuma Parçası: Lezzetli Meyveler", "content": """Doğanın renkli sofrasına hoş geldiniz! Bizler, dallarda güneşle olgunlaşan, her biri ayrı bir şifa kaynağı olan lezzetli meyveleriz. Sizinle tanışmak ve size güç vermek için sabırsızlanıyoruz.

Elma: "Benim adım Elma. En çok Amasya’nın bağlarını severim ama dünyanın her yerinde yetişirim. Kıpkırmızı, sapsarı ya da kütür kütür yeşil olabilirim. İçimde bolca lif ve vitamin taşırım. Beni her gün bir kez ısırarak yiyen çocukların dişleri temizlenir, yanakları al al olur. Unutmayın, ben sağlığın en yakın dostuyum!"

Armut: "Benim adım Armut. Şeker gibi tatlı, sulu bir yapım vardır. Şeklim bir çana benzer. Eğer kendinizi yorgun hissederseniz, hemen bir armut yiyin; çünkü ben size enerji verir, midenizi rahatlatırım. Yumuşak dokumla en seveceğiniz arkadaşınız olmaya adayım."

Portakal: "Benim adım Portakal. Kış geldiğinde, o gri havalarda turuncu rengimle içinizi ısıtırım. Akdeniz’in sıcak güneşini içimde saklarım. En büyük özelliğim, içinde sakladığım bolca C vitaminidir. Sizi kışın hapşırmaktan, öksürmekten ve soğuk algınlığından bir kalkan gibi korurum."

Üzüm: "Benim adım Üzüm. Salkım salkım dallarda asılır, güneşin tadını çıkarırım. Siyahım, morum, yeşilim... Her rengimle ayrı bir şifayım. Kurutulup çerez olurum, kaynatılıp pekmez olurum. Kan yaparım, zihninizi açarım. Ders çalışırken bir avuç kuru üzüm yemek, size ihtiyacınız olan zekayı ve enerjiyi verir."

Muz: "Benim adım Muz. Uzaklardan, sıcak iklimlerden gelirim. Yumuşacık tadımla çocukların en sevdiği meyvelerden biriyim. Kaslarınızı güçlendirir, boyunuzun uzamasına yardımcı olurum. Spor yaptıktan sonra beni yerseniz, kaybettiğiniz enerjiyi hemen geri kazanırsınız."

Bizler toprağın, suyun ve güneşin çocuklarıyız. Hepimizin tadı farklı olsa da amacımız aynı: Siz çocukların sağlıklı, güçlü ve neşeli büyümesine yardımcı olmak. Tabağınızdan meyveyi, yüzünüzden gülücüğü eksik etmeyin!"""},
            
            2: {"title": "2. Okuma Parçası: Dünya'nın Ateşi Mi Çıktı?", "content": """Deniz, o akşam televizyonda hava durumunu izlerken sunucunun bir cümlesine çok şaşırmıştı: "Dünyamızın ateşi her geçen gün biraz daha yükseliyor." Deniz, ateşi çıktığında annesinin alnına ıslak bez koyduğunu ve dinlenmesi gerektiğini biliyordu. Peki, koca Dünya’nın ateşi nasıl düşerdi?

Ertesi gün okulda öğretmeni "Küresel Isınma" konusunu anlatırken Deniz hemen parmak kaldırdı: "Öğretmenim, Dünya gerçekten hasta mı oldu?" diye sordu. Öğretmeni gülümseyerek, "Aslında Dünya bize bir işaret veriyor Deniz," dedi. "İnsanlar çok fazla yakıt tükettiğinde, ağaçları kestiğinde ve çöplerini doğaya bıraktığında, havada görünmez bir battaniye oluşuyor. Bu battaniye, güneşin sıcaklığını hapsettiği için gezegenimiz terlemeye başlıyor."

Deniz, buzulların eridiğini ve kutup ayılarının evsiz kaldığını öğrendiğinde çok üzüldü. Ama öğretmeni ona bir müjde verdi: "Dünya’yı iyileştirecek olan ilaç biziz!"

Eve dönerken Deniz neler yapabileceğini düşündü. İlk iş olarak dişlerini fırçalarken suyu boşuna akıtmadı. Odasından çıkarken ışığı kapattı. Babasına, markete giderken araba yerine yürümeyi teklif etti. Arkadaşlarıyla bir araya gelip bahçeye küçük fidanlar diktiler. Her fidan, Dünya’nın nefes almasını sağlayan taze birer soluk gibiydi.

Deniz artık biliyordu; plastik kullanmamak, geri dönüşüm yapmak ve ormanları korumak, Dünya’ya verilen en güzel hediyeydi. Biz gezegenimizi seversek, o da bize pırıl pırıl gökyüzü ve serin denizlerle teşekkür ederdi. Deniz, o gece yatağına yattığında gökyüzündeki yıldızlara baktı ve fısıldadı: "Korkma güzel Dünya, biz senin yanındayız ve ateşini hep birlikte düşüreceğiz!"""},
        
            3: {"title": "3. Okuma Parçası: Kümesin İçindekiler", "content": """Güneş henüz dağların arkasından yeni doğmuştu. Küçük Elif, köydeki evlerinin bahçesinde her sabah yaptığı gibi en sevdiği yer olan kümese doğru heyecanla koştu. Kümesin kapısına yaklaştığında içeriden gelen tuhaf sesleri duydu: "Tık, tık, tık..."

Normalde tavukların neşeli gıdaklamalarını duymaya alışıktı ama bu ses çok farklıydı. Elif, "Kümesin içinde ne var acaba?" diye düşünerek kapıyı yavaşça araladı. İçerisi biraz loştu. Gözleri alışınca, en köşede samanların üzerinde oturan anne tavuk Pamuk’u gördü. Pamuk, her zamankinden daha sakin ve dikkatli duruyordu.

Elif parmak uçlarında yürüyerek yaklaştı. Tam o sırada Pamuk’un kanatlarının altından sarı, yumuşacık bir kafa uzandı. Bu küçük, minicik bir civcivdi! Hemen ardından bir tane daha, sonra bir tane daha çıktı. Civcivler, "cik cik" diyerek annelerinin etrafında dönmeye başladılar. Elif’in merakı yerini büyük bir sevince bırakmıştı.

"Demek o tık tık sesleri, sizin yumurtadan çıkma çabanızdı!" diye fısıldadı Elif. Civcivler o kadar küçüktü ki, adeta yürüyen sarı pamuk şekerlere benziyorlardı. Elif hemen mutfağa koşup dedesinden yardım istedi. Birlikte taze yemler ve küçük bir kapta su hazırladılar."""},
           
            4: {"title": "4. Okuma Parçası: Mavi Sahilin Dostları", "content": """Güneş, masmavi denizin üzerinde pırıl pırıl parlıyordu. Kerem, o sabah erkenden kalkmış, dedesinin küçük teknesiyle denize açılmak için sabırsızlanıyordu. "Mavi Sahil" dedikleri bu kıyı, bembeyaz kumları ve berrak suyuyla kasabanın en sevilen yeriydi.

Sahile indiklerinde Kerem, kumların üzerinde renkli ama oraya ait olmayan bazı şeyler fark etti: Plastik şişeler, poşetler ve eski bir file parçası... Denizin dalgaları, bu yabancı maddeleri kıyıya vuruyordu. Kerem’in neşesi biraz kaçmıştı. Dedesine dönerek, "Dede, deniz neden bu kadar yorgun görünüyor?" diye sordu.

Dedesi gülümseyerek Kerem'in omzuna dokundu. "Deniz yorgun değil evladım, sadece bizden yardım bekliyor. Eğer biz ona iyi bakmazsak, içindeki dostlarımız; balıklar, yunuslar ve deniz yıldızları evsiz kalır," dedi.

Birlikte hemen işe koyuldular. Kerem eline büyük bir çöp torbası aldı. Kumların arasındaki plastikleri bir bir toplarken, küçük bir yengecin bir poşetin altına sıkıştığını gördü. Nazikçe poşeti kaldırdı ve yengecin özgürce suya koşmasını izledi. O an anladı ki, her küçük çöp aslında bir canlının yaşamını zorlaştırıyordu.

Birkaç saat sonra sahil, eski pırıltısına kavuşmuştu. Kerem ve dedesi teknelerine binip biraz açıldılar. Denizin altı rengârenkti. Kerem, suyun içindeki süzülen balıkları izlerken doğayı korumanın ne kadar önemli olduğunu bir kez daha fark etti. "Mavi Sahil artık gerçekten mavi!" diye bağırdı mutlulukla.

O gün Kerem bir söz verdi: Sadece kendi çöpünü değil, doğada gördüğü her fazlalığı temizleyecek ve arkadaşlarına denizlerin bizim en büyük hazinemiz olduğunu anlatacaktı. Çünkü temiz bir dünya, mutlu çocukların ve özgürce yüzen balıkların dünyasıydı."""},
            
            5: {"title": "5. Okuma Parçası: Sihirli Kostüm Dolabı", "content": """Yağmurlu bir pazar günüydü. Arda ve Zeynep, dışarı çıkamadıkları için evde biraz sıkılmışlardı. Tam o sırada anneleri gülümseyerek yanlarına geldi. "Çocuklar, çatı katındaki eski ahşap dolabı hatırlıyor musunuz? İçinde babanızla benim çocukluğumuzdan kalma pek çok giysi var. Belki orada kendinize yeni bir dünya kurabilirsiniz," dedi.

İki kardeş merakla çatı katına çıktılar. Tozlu rafların arasında duran koca dolabı açtıklarında gözlerine inanamadılar. Bu sadece bir dolap değil, sanki bir zaman makinesiydi! En üstte parlak, gümüş renkli bir pelerin duruyordu. Arda pelerini sırtına geçirdiği an kendini uzak bir gezegende, yıldızların arasında keşif yapan bir astronot gibi hissetti. "Bak Zeynep! Ben Galaksi Kaşifi Arda! Evrenin gizemlerini çözmeye gidiyorum!" diye bağırdı.

Zeynep ise dolabın alt çekmecesinde renkli, çiçekli büyük bir şapka ve eski bir çanta buldu. Şapkayı başına takınca birden dünyayı dolaşan bir gezgin oluverdi. "Ben de kıtaları aşan, yeni diller öğrenen ve çocuklara masallar anlatan Gezgin Zeynep!" diyerek abisine eşlik etti.

Bir süre sonra dolaptan çıkan eski bir doktor önlüğü Arda’yı bir araştırmacıya, uzun bir şal ise Zeynep’i bir iyilik perisine dönüştürdü. Giydikleri her kıyafet onlara farklı bir karakterin kapısını açıyordu. Kostümler değiştikçe ses tonları, yürüyüşleri ve bakış açıları da değişiyordu. Bir itfaiyeci olduklarında cesareti, bir öğretmen olduklarında ise sabrı ve paylaşmayı hayal ettiler.

O gün yağmur hiç dinmedi ama Arda ve Zeynep bir saniye bile sıkılmadılar. Bir kostüm dolabının yardımıyla, sadece odalarının içinde dünyayı gezdiler, gökyüzüne çıktılar ve en önemlisi başkalarının yerine kendilerini koymayı öğrendiler. Akşam olduğunda kostümleri yerine özenle yerleştirirken şunu fark ettiler: En büyük yetenekleri dolaptaki giysiler değil, kendi hayal güçleriydi."""},
        
            6: {"title": "6. Okuma Parçası: Küçük Ayının Kış Sorusu", "content": """Ormanda ağaçlar sarı ve turuncu yapraklarını birer birer dökmeye başlamıştı. Soğuk rüzgarlar esiyor, kışın habercisi bulutlar gökyüzünü kaplıyordu. Küçük ayı Pofuduk, annesinin büyük bir özenle hazırladığı mağaraya bakıp iç geçirdi. Annesi, "Haydi Pofuduk, uzun bir uyku vakti yaklaşıyor," dediğinde, Pofuduk’un aklında tek bir soru vardı: "Bu kış hiç uyumasak olmaz mı?"

Pofuduk, kışın yağan karla oynamak, donmuş gölün üzerinde kaymak ve arkadaşı tavşanla saklambaç oynamak istiyordu. Annesine, "Neden uykuda bütün eğlenceyi kaçırıyoruz?" diye sordu.

Annesi, Pofuduk’u yanına çağırdı ve yumuşak bir sesle anlatmaya başladı: "Bak küçük yavrum, doğa kışın derin bir dinlenmeye çekilir. Kar toprağı bir yorgan gibi örterken, yiyecek bulmak zorlaşır. Biz ayılar, baharda daha güçlü ve sağlıklı uyanmak için bu uzun uykuya ihtiyaç duyarız. Eğer uyumazsak, enerjimiz biter ve hastalanabiliriz."

Pofuduk biraz düşündü. "Peki, rüyalarımızda ne göreceğiz?" dedi merakla. Annesi, "Rüyalarımızda çiçeklerin açtığı baharı, neşeyle akan dereleri ve bal kovanlarını göreceğiz. Uyandığımızda ise her yer yemyeşil olacak," diye cevap verdi.

Pofuduk, annesinin söylediklerini duyunca kış uykusunun aslında bir kayıp değil, güzel bir hazırlık olduğunu anladı. Mağaranın içindeki yumuşak yapraklardan yapılmış yatağına uzandı. Dışarıda ilk kar taneleri yere düşerken, Pofuduk esnemeye başlamıştı bile. Gözlerini kapatırken aklında karda oynamak değil, baharda uyanacağı o muhteşem orman vardı.

Kış uykusu, sadece ayılar için değil, tüm doğa için bir dinlenme zamanıydı. Pofuduk derin bir uykuya dalarken, kalbinde baharın umudu ve annesinin sıcaklığı vardı. Orman sessizliğe bürünmüş, yeni bir başlangıç için beklemeye koyulmuştu."""},
        
            7: {"title": "7. Gökyüzündeki Ortak Renkler:", "content": """Rüzgarlı bir bahar sabahıydı. Mert, babasıyla birlikte yaptığı kıpkırmızı uçurtmasını kapıp mahalledeki geniş parka koştu. Uçurtmasının kuyruğu gökkuşağı gibi renkliydi. Mert, "Bugün en yükseğe benim uçurtmam çıkacak!" diye düşünüyordu.

Parkın diğer ucunda ise Selin vardı. Selin'in uçurtması da masmaviydi ve üzerinde bembeyaz bulut resimleri vardı. İki çocuk da uçurtmalarını havalandırmak için rüzgarı beklemeye başladılar. Tam rüzgar çıktığında ikisi de aynı anda koşmaya başladı. Ancak bir sorun vardı; uçurtmaların ipleri birbirine dolanıverdi!

Mert sinirle, "Benim yoluma çıktın, şimdi uçurtmam yere düşecek!" dedi. Selin ise üzülerek, "Asıl sen benim önüme geldin, mavi uçurtmamın ipi düğüm oldu," diye cevap verdi. İkisi de bir süre ipleri çözmeye çalıştı ama ipler daha da karıştı. O sırada uçurtmalar yan yana, rüzgarda çırpınarak sanki birbirlerine sarılmış gibi görünüyorlardı.

Mert'in dedesi çocukların yanına geldi ve nazikçe gülümsedi. "Bakın çocuklar," dedi. "Eğer ipleri birbirinizden çekmeye devam ederseniz ikisi de kopar. Ama birlikte hareket ederseniz, gökyüzünde iki kat daha güçlü bir renk şöleni oluşturabilirsiniz."

Mert ve Selin birbirlerine baktılar. Haklıydı. Önce ipleri sabırla çözdüler, sonra da uçurtmalarını birbirlerine çok yakın ama birbirine engel olmayacak şekilde aynı anda havaya saldılar. Şimdi gökyüzünde bir kırmızı, bir mavi uçurtma dans ediyordu. Mert ve Selin ise artık tartışmıyor, uçurtmaların süzülüşünü izlerken kahkahalar atıyorlardı.

O gün Mert ve Selin harika bir şey öğrendi: Tek başına uçurulan bir uçurtma güzeldi ama bir dostla paylaşılan gökyüzü çok daha eğlenceliydi. Parktan ayrılırken artık "benim uçurtmam" demiyorlar, "bizim uçurtmalarımız" diyorlardı."""},
           
            8: {"title": "8. Okuma Parçası: Bir Yumak", "content": """Ece’nin kedisi Pamuk, dünyanın en meraklı kedisiydi. Beyaz tüyleri, yeşil gözleri ve hiç durmadan hareket eden kuyruğuyla evin neşesiydi. Bir kış akşamı Ece’nin annesi, kucağında rengârenk yünlerle salona geldi. Ece’ye sıcacık bir atkı örmek için hazırlık yapıyordu.

Annesi masanın üzerindeki sepetten kırmızı bir yumağı çıkardığında, Pamuk’un kulakları dikildi. Kırmızı yumak, sanki Pamuk’a "Hadi gel, benimle oyna!" diyordu. Annesi çay demlemek için mutfağa gittiği an, macera başladı. Pamuk, tek bir hamleyle yumağa pençe attı. Yumak masadan yuvarlandı, koltuğun altına girdi, oradan fırlayıp koridorun sonuna kadar kaçtı.

Pamuk, yumağın peşinden koşarken kırmızı ip evin her yerine dolanmaya başladı. Sandalyelerin bacakları, sehpanın kenarları ve Ece’nin yerdeki oyuncak kamyonu artık kıpkırmızı bir ağla kaplanmıştı. Ece odaya girdiğinde gördüğü manzaraya inanamadı. Her yer kırmızı iplerle doluydu ve Pamuk, ipin ucuna dolanmış halde "Miyav!" diyerek yardım bekliyordu.

Ece önce biraz şaşırdı, sonra bu komik duruma gülmeye başladı. "Seni yaramaz Pamuk! Atkımı örmeden bitirmişsin bile," dedi. Hemen annesini çağırdı. Birlikte, Pamuk’u incitmeden iplerden kurtardılar. Ardından ipleri geri sarmaya başladılar. Ece yumağı sarıyor, annesi de düğümleri çözüyordu. Pamuk ise yaptığı işten çok memnunmuş gibi köşesine çekilip patilerini yalamaya başlamıştı.

O akşam atkı hemen bitmedi ama Ece ve annesi ipleri sararken çok eğlendiler. Ece, hayvan dostlarının merakının bazen küçük kazalara yol açabileceğini ama onlara sabırla yaklaşmak gerektiğini öğrendi. Pamuk ise o geceden sonra yün sepetine sadece uzaktan bakmaya karar verdi. Çünkü o, artık kendi oyuncağı olan küçük fareyle oynamanın daha güvenli olduğunu biliyordu."""},
           
            9: {"title": "9. Okuma Parçası: Altın Renkli Orman", "content": """Can, o sabah penceresinden dışarı baktığında bahçedeki büyük çınar ağacının renginin değiştiğini fark etti. Daha birkaç hafta önce yemyeşil olan yapraklar, şimdi altın sarısı ve turuncuya bürünmüştü. Babası, "Hadi Can, bugün ormanda küçük bir sonbahar yürüyüşüne ne dersin?" diye sorunca Can neşeyle ayakkabılarını giydi.

Ormana vardıklarında hava serin ama tazeydi. Bastıkları yerler çıtır çıtır ses çıkarıyordu. Can yere baktığında, toprağın kurumuş yapraklardan yapılmış doğal bir halıyla kaplandığını gördü. "Baba, ağaçlar neden elbiselerini yere döküyor?" diye sordu.

Babası bir yaprağı eline alarak, "Aslında ağaçlar uykuya hazırlanıyor Can," dedi. "Kış gelmeden önce enerji toplamak için yapraklarını bırakırlar. Bu yapraklar toprakta çürüyerek diğer bitkilere besin olur. Yani doğada hiçbir şey boşa gitmez."

Yürürken bir sincabın ağzında kocaman bir palamutla koşturduğunu gördüler. Sincap, telaşla palamudu bir ağacın kovuğuna saklıyordu. Can, sincabın kış için hazırlık yaptığını hemen anladı. Sonbahar, sadece ağaçlar için değil, ormandaki tüm canlılar için bir hazırlık mevsimiydi.

Can, yol boyunca farklı şekillerde yapraklar topladı. Kimi kalp şeklinde, kimi ise yıldız gibiydi. Bir ara rüzgar sertçe esti ve havada uçuşan yapraklar tıpkı renkli kelebekler gibi dans etmeye başladı. Can bu manzarayı izlerken doğanın ne kadar büyük bir sanatçı olduğunu düşündü.

Eve döndüklerinde Can, topladığı yaprakları bir defterin arasına yerleştirdi. Artık biliyordu ki dökülen her yaprak, baharda açacak olan yepyeni çiçeklerin habercisiydi. Sonbahar bir veda değil, doğanın dinlenmek için nazikçe hazırlandığı huzurlu bir mevsimdi."""},
       
            10: {"title": "10. Okuma Parçası: Tavşan Köyü'nün Sırrı", "content": """Yemyeşil tepelerin ardında, çiçeklerin mis gibi koktuğu huzurlu bir vadi vardı. Burası, kulakları uzun, burunları ise sürekli hareket eden sevimli canlıların yaşadığı "Tavşan Köyü"ydü. Köyün her köşesinde küçük, pencereli toprak evler ve bu evlerin önünde taze havuçların yetiştirildiği minik bahçeler bulunurdu.

Tavşan Köyü’nün en önemli kuralı, herkesin birbirine yardım etmesiydi. Bir sabah, köyün en meraklı tavşanı Hopzıpla, vadinin girişinde büyük bir kayanın devrildiğini gördü. Bu kaya, tavşanların su içtiği dereye giden yolu kapatmıştı. Hopzıpla hemen köyün meydanına koşup arkadaşlarına haber verdi. "Arkadaşlar, dereye ulaşamıyoruz! Yardımlaşma vaktidir!" diye bağırdı.

Çok geçmeden tüm tavşanlar ellerinde kürekler ve tırmıklarla bir araya geldiler. Küçük tavşanlar etraftaki çalıları temizlerken, büyük tavşanlar kayayı yerinden oynatmak için plan yaptılar. Bilge Tavşan Akbaş, "Eğer hepimiz aynı anda, aynı yöne itersek başarılı olabiliriz," dedi.

Tüm tavşanlar yan yana dizildi. Hep bir ağızdan "Bir, iki, üç!" diyerek kayaya omuz verdiler. İlk denemede kaya sadece biraz kımıldadı. Ama tavşanlar pes etmedi. İkinci denemede, dayanışmanın verdiği güçle koca kaya yerinden yuvarlanıverdi. Yol açılmış, dere yeniden neşeyle akmaya başlamıştı.

O gün Tavşan Köyü'nde büyük bir şölen yapıldı. Tavşanlar en taze marullarını ve kıtır havuçlarını sofraya getirdiler. Birlikte yemek yerken tek bir tavşanın yapamayacağı bir işi, koca bir köyün nasıl kolayca başardığını konuştular. Akşam olup güneş batarken, Tavşan Köyü'nde sadece suyun sesi değil, dostluğun ve birliğin huzuru duyuluyordu. Hopzıpla o gece yatağına yatarken şöyle düşündü: "Birlikteyken bizden daha güçlüsü yok!"""},
           
            11: {"title": "11. Okuma Parçası: Mavi Dalgaların Sırrı", "content": """Deniz kıyısında yaşayan Ada için en büyük eğlence, hafta sonları babasıyla birlikte iskeleye gidip denizi izlemekti. Deniz bazen masmavi, bazen yemyeşil olur; dalgalar kıyıya küçük hediyeler bırakırdı. Ancak o sabah Ada, iskeleye vardığında gördüklerine çok üzüldü. Su o kadar bulanıktı ki balıkları seçmek imkansızdı. Üstelik suyun üzerinde poşetler ve boş kutular yüzüyordu.

Ada, "Baba, deniz bugün neden bizimle konuşmuyor?" diye sordu. Babası üzüntüyle denize baktı. "Çünkü denizimiz şu an çok yorgun Ada. İnsanlar bazen çöplerini ait olmadıkları yerlere bırakıyorlar. O çöpler nehirlerle denize ulaşıyor ve oradaki canlıların evini kirletiyor," dedi.

Tam o sırada Ada, kıyıya yakın bir yerde çırpınan küçük bir gümüş balığı fark etti. Balık, şeffaf bir plastik parçasının arasına sıkışmıştı. Ada hemen babasından yardım istedi. Babası balığı nazikçe sudan çıkarıp plastikten kurtardı ve tekrar özgürlüğüne kavuşturdu. Gümüş balığı, sanki teşekkür eder gibi kuyruğunu sallayarak derinlere süzüldü.

Bu olay Ada’yı harekete geçirdi. Ertesi gün okula gittiğinde arkadaşlarına ve öğretmenine gördüklerini anlattı. Hep birlikte bir "Temiz Deniz Elçileri" grubu kurdular. Hafta sonu aileleriyle birlikte sahilde büyük bir temizlik etkinliği düzenlediler. Sadece çöpleri toplamakla kalmadılar, sahilin girişine "Deniz Canlıların Evidir, Lütfen Evimizi Temiz Tutalım" yazılı renkli tabelalar astılar.

Birkaç hafta sonra deniz eski berraklığına kavuşmuştu. Ada iskeleden baktığında, kurtardığı gümüş balığının arkadaşlarını bile görebiliyordu. Artık biliyordu ki denizi korumak, sadece kıyıdaki çöpleri toplamak değil, hiçbir çöpün suya ulaşmasına izin vermemekti. Temiz bir deniz, sadece balıklar için değil, kıyıda oynayan tüm çocuklar için de en büyük mutluluktu."""},
        
        12: {"title": "12. Okuma Parçası: Ormanın Görkemli Dansı", "content":"""Baharın gelişmesiyle birlikte koca orman, derin uykulardan çıkmak. Rüzgâr, ağaç dallarının aralarındaki parçalar sanki birbirleriyle gizli bir şeyler fışkırıyordu. Küçük sincap Fındık, bir ağacın kovuğundan farklılaştığı ve bugünün diğer günlerinin farklı olduğu hemen aydınlatılıyor. Bugün, ormanın geleneksel "Bahar Dansı" günüydü!

Gökyüzünde süzülen kuşlar, en güzel şarkılarının boyutları görülüyor. Dere, taşların üzerinden atlarken "şırıl şırıl" sesiyle bu şarkıya eşlik ediyordu. Fındık, elindeki iki meşe palamudunu içeren vurarak ritmi tutturdu: Tık, tık, tık! Bu sesler duyan diğer hayvanlar da birer birer orman meydanına dönmeye başladı.

Ormanın en yaşlı ve bilgili ağacı Çınar Dede, dallarını ağır ağır sallayarak dansın gideceğini haber verdi. Tavşanlar neşeyle zıplıyor, kelebekler rengarenk kanatlarını çırparak havada zarif daireler çiziyordu. Ayı Koca Pençe ise ayaklarını yerde "güm güm" diye vurarak ormanın davulcusu olmuştu. Onun canlı, kendi yeteneğiyle bu muhteşem orkestranın bir parçasıydı.

Fındık, arkadaşı Yavaş'ın biraz kenarda desteğini gördü. Yavaş, diğerleri bir o kadar da hızlı dans edemediği için üzülüyordu. Fındık hemen yanına gitti. "Bak Yavaş" dedi, "Herkesin dansı farklıdır. Önemli olan hızı değil, kalbinin müzik dağılmasıdır." Yavaş yavaş yürümeye ve kendi ritmiyle başını sallamaya başladı. Bir ormandaki uyum mükemmel bir hâle geldi.

Güneş batarken ormanın köşesinden huzurlu bir melodi yükseliyordu. Doğa, yalnızca ağaçlardan ve hayvanlardan oluşmaktaydı; O, hep birlikte söylenen dev bir şarkı gibiydi. Fındık ve arkadaşları yorulmuş ama çok mutlu olmuşlardı. Ormanın dansı bitmişti ama o güzel melodi, tüm çocukların hayallerinde yaşamaya devam edecekti."""},
        
        13: {"title": "13. Okuma Parçası: En Lezzetli Kurabiye", "content":"""Cumartesi sabahı Selin, mutfaktan gelen mis gibi kokularla ortaya çıkıyor. Annesi mutfağında, Selin'in en sevdiği üzümlü kurabiyeleri pişiriyordu. Fırından yeni çıkan kurabiyeler altın sarısı gibi parlıyor, üzerindeki minik kuru üzümler adeta gülümsüyordu.

Selin heyecanla filtrelemeye girdi. "Anneciğim, hepsini yiyebilir miyim?" diye sordu. Annesi gülümseyerek, "Tabii ki yiyebilirsin Selin ama yiyebilirsin, lezzetler paylaştıkça çoğalır" dedi. Selin bu cümleyi biraz düşündü. O sırada yan komşular Fatma Teyze'nin hastalandığını ve birkaç yerde dışarıda çıkmadığını hatırladı.

Selin, en güzel tabaklardan birini seçti. İçine bereketli altı tane üzümlü kurabiye yerleştirildi. Üzerini beyaz bir peçeteyle kapattı. Annesinden izin alıp Fatma Teyze'nin kapağını çalar. Kapıyı açan Fatma Teyze biraz yorgundu ama Selin'i ve elindeki tabağı kırsal gözlerinin içi parladı. "Ah Selin! Bu güzel koku bütün eve gidiyor, ne kadar naziksin" dedi.

Selin eve sunulan kurabiyelerden bir tanesini aldı. çevredeki bir şey vardı; Kurabiye her şeyin çok daha lezzetli olması. Annesine dönerek, "Haklıydın anne! Paylaştığım için mi tadı böyle güzelleşti?" diye sordu. Annesi Selin'in saçlarını okşayarak, "Evet Selin. Çünkü o kurabiyenin içine sadece üzüm değil, sevgi ve düşüncelilik de karıştı," cevabını verdi.

O sürenin ardından Selin, arkadaşı Arda'yı da bahçeye çağırdı. Kurabiyelerini onunla da paylaştı. Birlikte kurabiye yerken kurdukları oyunlar, her şeyi daha eğlenceliydi. Selin o günün önemli bir şeyi: Tek başına yenen en tatlı yemek bile, birinin sevilen ikramı olan küçücük bir parçanın dünyasında mutluluk olamazdı. Paylaşmak, dünyanın en sihirli malzemesiydi."""},

        14: {"title": "14. Okuma Parçası: Geceyi Aydınlatan Küçük Işık", "content":"""Yaz mevsiminin ılık gecelerinde, ormanın derinliklerinde sihirli bir hazırlık başlıyordu. Gökyüzünde yıldızlar pırıl pırıl parlarken, yerdeki çalıların arasında da minik yıldızlar yükselirdi. Bunlar, karınlarındaki fenerleriyle geceyi aydınlatan ateş böcekleriydi.

Küçük ateş böceği Parıltı, o gece ilk uçuş için çok heyecanlıydı. Diğer arkadaşları sarı ve yeşil ışıklar saçarak havada süzülüyor, sanki karanlık gökyüzüne birer imza atıyorlardı. Parıltı da kanatlarını çırptı ve kendi ışığını yaktı. Fakat bir gariplik vardı; Parıltı'nın ışın diğerlerininkinden biraz daha farklı, hafif turuncu bir tondaydı.

Parıltı bir an duraksadı. "Acaba ışığım yanlış mı yanıyor? Neden herkes gibi değilim?" diye düşündüm ve bir yaprağın üzerine konup ışığını söndürdü. O sırada ormanın en yaşlı baykuşu Bilge Kanat, ağacın sahibinin Parıltı'yı izliyordu. "Küçük dostumdan saklanıyor musun?" diye sordu Baykuş.

Parıltı bereketce, "Işığım diğerleri gibi değil, ben muhtemelen dansı bozuyorum" dedi. Sintine Kanatlarının kanatlarını hafifçe hareket ettirerek yürümeye başladı. "Bak Parıltı, ormana bir bak! Çiçeklerin hepsi aynı renk mi? Ya da tüm kuşların aynı şarkıları mı diyor? Eğer herkes aynı olsaydı, dünya bu kadar güzel bir yer olur. Senin turuncu ışığın, bu geceki dansın en özel parçası."

Parıltı bu sözler üzerine derin bir nefes aldı ve tekrar yayınlandı. Kendi rengi sevgiyle kucaklayarak gökyüzüne yükseldi. Sarı, yeşil ve turuncu ışıklar bir araya gelince orman, tarihin en renkli ve en uyumlu dansına tanıklık etti. Parıltı o gece aydınlatması ki; gerçek güzelliğin ortaya çıkması benzemekte değil, kendi ışığını cesaretle tüm dünyada sunmaktaydı.

Güneş doğarken tüm ateş böcekleri yuvalarına geri döndü. Parıltı artık biliyordu; Onun canlı, doğa dev tablosundaki olağandışı bir fırça darbesiydi ve onun ışığının tam da olması gerekiyordu."""},

        15: {"title": "15. Okuma Parçası: Renkli İplerin Hikayesi", "content":"""Anadolu'nun küçük ve şirin bir köyünde, Elif'in babasıannesi Zeynep Hanım'ın evinde her sabah neşeli sesler yükselirdi. Evin ortasında muazzam bir halı tezgahı duruyordu. Zeynep Hanım, bu yıl köyün okul ücreti için büyük ve yumuşak bir halı dokumaya karar sözü. Ancak bu halı biraz farklıydı; adı "Yardımlaşma Halısı"ydı.

Zeynep Hanım, köydeki herkese haber saldı: "Elinde bir yumak ipi olan, gönlünde bir sevgi olan gelsin!" Çok miktarda Elif ve arkadaşları, ellerinde farklı oranlarda iplerle çıkageldiler. Kimi deniz mavisi bir yün, kimi güneş sarısı bir yumak, kimi de orman yeşili bir ip getirmişti.

Babaanne tezgahın başına geçti ve düğüm atmayı yetiştirmeye başladı. "Bakınlarım" dedi, "Tek bir ip zayıftır ama bu ipler birbirine düğümlenip yana yana kırılması bir imkansız halıya dönüşür. bizim gibi..." Elif, kırmızı ipini test edilmiş ilmeklerin arasında kalmıştı. Arkadaşı Kerem yanındaki şampiyon sarı ipi ekledi.

Günlerdeki halı büyüdü. Üzerinde sadece renkler değil, çocukların karşılıklı masalları, yapılan sohbetler ve ekmeklerin huzuru da mevcuttu. Kimse "benim ipim daha güzel" demiyordu, herkes "bizim halımız ne zaman bitecek?" diye soruyordu. Halının üstündeki desenler, köydeki herkesin emeğini bir çiçek bahçesi gibi yansıtıyordu.

Kütüphanenin açıldığı gün, halı en güzel köşeye serildi. Çocukların üzerinde kaldıklarında sadece yumuşacık bir zemin değil, birlikte bir şeylerin başarıldığını hissediyorlar. Elif o günün aydınlatması ki; Dünyayı güzelleştiren şey sadece renkli ipler değil, o iplerin sahip olduğu sevgi ve yardımlaşmaydı. O gün sonra köyde ne zaman zor bir iş olsa herkes bir ilmek atmak için bir araya geldi. Çünkü biliyorlardı ki; El ele verildiğinde onun zorluğu, rengârenk bir halıya dönüştü."""},

        16: {"title": "16. Okuma Parçası: Mis Gibi Orman Yolculuğu", "content":"""Mert'in sınıfı o gün çok heyecanlıydı. Öğretmenleri Hanife Hanım, onların kasabanın hemen dışındaki çam ormanına bir yolculuk gezisine götüreceğini söylemişti. Mert, çantanı hazırlarken bir yığın ve küçük bir not defteri koydu. Amacı, ormandaki minik canlıları ve ilginç ayrıntıların çoğaltılmasıdır.

Ormanın girişine vardıklarında onları "mis gibi" bir çam kokusu verir. Kuş sesleri, ağaçlarının hışırtısına karışıyordu. Ancak Mert'in yüzü biraz yavaşladı. Yol boyunca uzanan çalılıkların arasında kağıt mendiller, meyve suyu programları ve piknikçilerden kalan plastik poşetler mevcuttu. Orman, o güzel kokuya rağmen biraz dağınık ve dağınıktı.

Hanife Öğretmen durdu ve çocuklara baktı. "Çocuklar, doğa bize nefes almamız için şık bir hava sunuyor. Peki, biz ona karşılığında ne veriyoruz?" diye sordu. Mert hemen şunu söyledi: "Öğretmenim, belki ormandan yardım istiyor. Bu çöpler buraya ait değil!"

Sınıfça bir karar aldılar. O günün sadece bozulma yapmayacak, aynı zamanda ormana bir hatıra hatıraları vereceklerdi. Öğretmenlerinin dağıttığı eldivenleri taktılar ve "Temizlik Takımı" işe koyuldu. Mert, bir ağacın kökünün farklı şekilde şekillenmiş şekilde çıkarırken altından küçük bir uğur böceğinin fırladığını gördü. "Bakın!" dedi arkadaşlarına, "Çöpleri temizledikçe dostlarımız evlerine kavuşuyor."

Kısa sürede orman, gerçekten "mis gibi" adına yakışır bir hale geldi. Topladıkları çöpleri poşetleyerek geri dönüşüm faaliyetlerine götürmek üzere ayırdılar. Ama içleri çok huzurluydu. Gezinin sonunda ağaçların altında çalıştırılmalarını yerken, tek bir kırıntı bile bırakmamaya özen gösterdiler.

Mert o gün defterine şu notu düştü: "En güzel orman, içinde ayak izlerimizden başka bir şey bırakmadığımız ormandır." Artık bildiği ki doğayı sevmeyi, onu sadece izlemek değil, ona bir çiçek gibi bakmak korumaktı."""},

        17: {"title": "17. Okuma Parçası: Müzedeki Gizli Bahçe", "content":"""Zeynep'in okulu o gün şehirdeki en büyük sanat müzesine bir gezi düzenlemişti. Zeynep, daha önce hiç müzeye gitmemişti. "Müze" denince gelenlerin sadece eski, tozlu eşyalarının olduğu sessiz bir yer olması gerekiyordu. Ancak müzenin büyük kapısından içeri adım atıldığı an yanıldı.

Öğretmenleri onları büyük bir salonun önüne çıkardı. Salonun duvarları devasa tablalarla kaplıydı. Zeynep, bir tablonun önünde durma ve hayranlıkla bakmaya başladı. Bu tabloda rengârenk çiçekler, yemyeşil yapraklar ve pırıl pırıl akan bir dere vardı. Sanki tablonun içinden çiçek kokuları gelebilir. Rehber yanlarına ilişkin dökümanlarına, "Çocuklar, bu tablonun adı 'Müzenin Çiçek Bahçesi'. Ressam, doğayı o kadar çok sevmiş ki onu sonsuza kadar yaşatmak için rutinle bu tuvale taşımış" dedi.

Zeynep tabloya bakıldığında, her bir fırça darbesinin bir çiçeğin yaprağını oluşturduğunu fark etti. Müze, sadece eski eşyaların korunduğu bir yer değil; ülkelerin, renklerin ve hayallerin sergilendiği geniş bir bahçeydi. Diğer arkadaşların da kendi favori tablolarını barındırıyorlardı. Kimi gökyüzündeki yıldızlara bakıyor, kimi ise sökük yıl önce yaşamış çocukların oyunlarını izliyordu.

Müze gezisinin sonunda öğretmenlerin çocukları küçük kağıtlar ve kalemler dağıttı. "Şimdi sıranızda" dedi. "Gördüğünüz bu bahçeden ilham alarak kendi hayalinizdeki dünyayı çizin." Zeynep kağıdına büyük, gülen bir güneş ve müzede görüldüğünde o güzel çiçeklerden bir buket çizdi.

Eve dönerken Zeynep, müzenin aslında geçmişle gelecek arasında kurulan sihirli bir köprünün yapılandırıldığı. Artık onun fidanının, çiçeğinin ve sanat eserinin korunması gereken birer hazine olduğu biliniyordu. O gün Zeynep müze için, sadece bir bina değil, bölümlerde hiç solmayacak bir çiçek bahçesi olmuştu."""},

        18: {"title": "18. Okuma Parçası: Parktaki Renkli Top", "content":"""Güneşli bir başlangıçtan sonraydı. Kerem ve babası, mahallenin parkına oynamaya gittiler. Kerem tam kaydırmaağa doğru koşuyordu ki çalılıkların arasında kapsamlı bir şey gördü. Yaklaştığında bu yepyeni, üzerinde sarı yıldızlar olan masmavi bir futbol topu olduğu fark etti.

Kerem heyecanla topu kucağına aldı. "Bak baba! Sahipsiz bir üst buldum!" diye bağırdı. Top o kadar güzel ki Kerem içinden "Keşke benim olsa" diye geçirdi. Tam o sırada parkın diğer ucundaki şişlik bir ses duyuldu. Küçük bir çocuk, bankaların adına ve ağaç diplerine bakarak bir şeyler arıyordu. Kerem ve babası ona doğru yaklaştılar.

Kerem, elindeki topu sakladı. Babası eğilerek sordu: "Bir şey mi kaybettin küçük dostum?" Çocuk, gözleri karşısındak cevap verdi: "Evet, yeni topumu buralarda kaybettim. Üzerindeki sarı yıldızlar vardı, babamın doğum günü anılarıydı."

Kerem bir an duraksadı. Eğer sustuysa üstte bulunamıyorsa. Ama çocuğun üzüntüsünü yaşayanların kalbi sızdı. Kendi en sevdiği oyuncağını kaybetse ne kadar üzüleceğini düşündü. Yavaşça topu çıkarır ve uzatır. "Sanırım aradığın top bu" dedi.

Küçük yaştaki vücutta bir gülümseme açtı. "Evet! Çok teşekkür ederim, onu bulduğuma çok sevindim!" dedi. kişilerin adı Emre'ydi. Emre topu aldı ama hemen gitmedi. Kerem'e bakarak, "Birlikte oynamak ister misin? Tek oynamaktan daha eğlenceli olur" dedi.

Kerem ve Emre o gün akşama kadar parkta birlikte en iyi oynadılar. Kerem eve dönerken topun sahibi değildi ama yeni bir arkadaş kazanmıştı. Babası, Kerem'in başını okşayarak "Bugün çok doğru bir şey yaptın Kerem. Dürüstlük ve paylaşım, en güzel oyuncaklardan bile daha değerlidir" dedi. Kerem mutluydu, çünkü dürüstlüğün getirdiği huzur, hiçbir oyuncağın veremeyeceği kadar sıcaktı."""},

        19: {"title": "19. Okuma Parçası: Uyku Serüveni", "content":"""Efe, oyun oynamayı çok seven, neşeli ve enerji dolu bir çocuktu. Ancak Efe'nin hiç sevmediği bir şey vardı: Uyku vakti! Annesi "Haydi Efe, dinlenme zamanı" dediğinde, Efe hep aynı cevabı verirdi: "Ama anne, uyursam bütün eğlenceyi kaçırırım! Belki ben uyurken oyuncaklarım canlanıyor ya da yıldızlar gizli bir parti veriyor."

Efe'ye göre uyumak, zaman geçtikten sonra başka bir şey değildi. Bir akşam babası, Efe'nin yerinde oturmuş ve ona küçük bir sır vermişti. "Biliyor musun Efe," dedi babası, "Vücudumuzdaki en sevdiğin uzaktan kumandalı araban gibi çalışır. Gün boyunca koştun, fırladın ve yeni şeylerin öğrendiğin. Şimdi pillerini doldurma zamanı. Eğer uyumazsan, göreceğin büyük maceralar için enerjin kalır."

Efe bu "pil doldurma" yansımasını biraz düşündü. Ama asıl ikna eden babasının bir sonraki cümlesiydi: "Ayrıca uyku, beynimizin rüya laboratuvarıdır. En güzel fikirler, en renkli oyunlar uyurken zihnimizde filizlenir. Uyumayan bir çocuk, kendi rüyası ülkesine giden biletler alınır."

O gece Efe, pillerini doldurmaya ve rüya laboratuvarına gitmeye karar verdi. Pijamalarını giydi, dişlerini fırçaladı ve yumuşacık uzamasına uzandı. Gözlerini kapattıklarında, oluşumların gerçekte büyümediğini, huzurlu bir düzen olduğunu fark etti. Çok değişkenlik gösteren derin bir arıza daldı.

Rüyasında uçan bir bisikletle bulutların arasında dolaştığını, dev çileklerden görülen bir adaya gittiğini gördü. Sabahın değişik ilk ışıklarıyla uyandığında, kendini hiç olmadığı kadar güçlü hissediyordu. Yataktan bir kahraman gibi fırladı. Artık biliyordu ki; iyi bir uyku, harika bir sabahın anahtarıydı. Efe o gün sonra sadece oyun oynatmak değil, maceralarına güç toplamak için uyumayı da çok sevdi."""},

        20: {"title": "20. Okuma Parçası: Küçük Kardeşim Mete", "content":"""Benim dünyamda en sevdiğiniz kişiyi sorsanız, size hemen küçük kardeşim Mete'nin adını söylerim. Henüz çok küçük, büyükleri parlak gözleri ve güldüğünde ortaya çıkan tek bir dişi var. Annem eve Mete'yi ilk getirdiğinde, "Artık sen bir ablasın, o sana emanet" dedi. O gün bu emanetin ne kadar değerli olduğunu araştırır.

Mete ile yaşamak bazen çok heyecanlı, bazen de biraz sabır istiyor. Mesela en sevdiğim boya kalemlerimi aldığında ya da tam verirken defterimin üzerine oturduğunda önce biraz şaşırıyorum. Ama sonra bana bakınca o neşeli kahkahalarını attığında, kızgınlığım bir dondurmanın güneşinde erimesi gibi yok olup gidiyor. Çünkü biliyorum ki o, sadece beni taklit etmek ve benimle oyun oynamak istiyor.

Mete'yi en çok uyurken izlemeyi seviyorum. Küçük parmaklarını yumruklamış, huzurla nefes alırken o kadar masum görünüyor ki... O uyurken odasının kapısını kapatıyor, ses yapmaya çalışmıyor. Bu, bir kardeşinin kardeşine sunabileceği en sessiz ve en güzel hediye bence.

Birlikte parka gittiğimizde ise ayrıcalıklı bir koruyucu gibi büyümek. Salıncakta sallanırken azalman diye duruyor, kum havuzunda ona en renkli kovaları uzatıyorum. Onun küçük adımlarıyla bana doğru koşması, "Abla!" diye seslenmeye çalışmasının tüm parçalarından daha değerli.

Bazen "Mete'yi neden bu kadar çok seviyorsun?" diye soruyorum kendim. Cevabı aslında çok basit: Kardeş demek, sevginin ikili tamamlayıcısı değil, tam kalbinin daha da gücü demekmiş. Mete benim sadece kardeşim değil; o benim en sadık oyun arkadaşım, en küçük sırdaşım ve hayat boyu burada olacak can dostum. İyi ki varsın Mete, seni çok seviyorum!"""},
        
        21: {"title": "21. Okuma Parçası: Sevgi'nin Renkli Halkaları", "content":"""Sevgi, her zaman farklı şeyleri düşünmeyi ve oyunlarına yeni dünyalara sığdırmayı çok yedi bir çocuktu. Bir süre sonra babası ona bir kutu içinde rengârenk, farklı boyutlarda halkalar dile getirildi. Bu halkalar ilk bakışta sadece basit plastik oyuncaklar gibi gösterildi. Ama Sevgi'nin elinde onlar, sihirli birer anahtara dönüştüler.

Sevgi, en büyük mavi halkayı eline aldı ve onu kaldırdı. "Bu benim dev sürdürülebilirim!" dedi kendi kendine. Bahçedeki çiçeklere, manipülasyonların süresine bu halkadan çalışmaya başladı. Mavinin halkanın içinden dünya çok daha heyecan verici bir şekilde aktarılır. Daha sonra kırmızı halkayı aldı ve onu belinde çevirmeye başladı. Şimdi o, bir sirkin ve yetenekli jimnastikçiydi!

Oyunun ilerlemesi Sevgi halkaları yere dizdi. Artık bu halkalar, içinden ziplenerek geçilen gizemli adalar olmuştu. Sarı halka sıcak bir ormanı, yeşil halka ise derin bir ormanı temsil ediyor. Sevgi bir adadan diğerine atlarken sadece fiziksel değil, hayalleri de güçleniyordu. "Hayatın sürdüğü ne kadar güzel" diye düşündü. "Bir halka bazen bir direksiyon, bazen bir taç, bazen de bir pencere olabiliyor."

Akşam olup güneş batmaya başladı Sevgi halkaları üst üste dizdi. Şimdi de renkli bir kule çalışması. Babasının yanından geçerek "Bugün halkalarla neler yaptın?" diye sorunca, Sevgi neşeyle yürüyordu. "Baba, onlar sadece halka değil; onları benim hayal halkalarım! Bugün dünyayı dolaştım, spor yaptım ve bir kâşif oldum."

Sevgi o gün bilgisi ki; Bir oyuncağın ne olduğu değil, ona hangi hayallerle ulaşmamız önemlidir. Sevgi'nin hayal halkaları, sınırlarının farklılığı ve gerçekliğin büyüklüğü ve büyük eğlence olduğu kanıtlandı. O gece uyurken bile halkalarının içinden geçerek yıldızlara ulaşan rüyalar gördü."""},
        
        22: {"title": "22. Okuma Parçası: Gizemli Parıltı", "content":"""Güneşli bir salı sonrasındaydı. Ali, okuldan sonra en sevdiği parka yayılmış, kum havuzunun kenarında küçük kamyonuyla oynuyordu. Tam o sırada, parktaki eski meşe ağacının soğuması arasında bir şeyin parladığını fark etti. Merakla yerinden ve yere doğru yürüdü.

Yaprakların saklanması, üzerinde gümüş renkli yıldızlar olan masmavi, özgürlüklü bir üst oluşumlar. Ali topu aldığında gözlerine inanamadı. Üst sanki elinde dans ediyor, ışık yansıtıyordu. "Vay canına!" dedi Ali. "Bu kadınların en güzel top!"

Ali topu hemen çantana sakladı. İçinden bir ses, "Bu top artık senin, bak kimse görmedi" diyordu. Ama bir başka ses de, "Ya bu topu birisi çok seviyorsa ve şu an üzülüyorsa?" diye fısıldıyordu. Ali o gün parkta topuyla oynamadı. Eve gittiğinde aksamalı top yatağının” koyduğu ama içi hiç rahat değildi. Akşam yemeğinde yemeğini bile kaçmıştı.

Ertesi gün parka tekrar gittiğinde, küçük bir kız çocuğunun ağacının altında ağladığını gördü. Kız, "Babamın uzaklardan yayımlanan sürümlü topumu kaybettim," bilgilerini paylaşıyordu. Ali'nin kalbi hızla çarpmaya başladı. O an, topun kendisinde değişmesi ona mutluluk değil, sadece ağır bir yük kendiliğinden anlaşılır.

Hemen koştu, top yatağının altına alındı ​​ve nefes nefese parka geri döndü. Topu küçük kıza uzatarak, "Bunu dün burada muhafaza ediyorsun, muhtemelen senin" dedi. Kızın vücudundaki o büyük mutluluk ve gözlerindeki pırıltılar, topun gümüş yıldızlarından bile daha parlaktı. "Çok teşekkür ederim! Adım Elif, her yerde birlikte oynayabiliriz" dedi.

Ali o gün Elif ile harika vakit geçirdi. Eve dönerken elleri boştu ama dürüstlüğünün verdiği huzurla dopdoluydu. Artık biliyordu ki; başkasına ait olan bir seçim bizi aydınlatmazdı, bizi asıl parlatan yaptığımız doğru davranışlardı."""},
        
        23: {"title": "23. Okuma Parçası: Sokaktaki Misafir", "content":"""Kış mevsiminin en soğuk günlerinden korunması. Melis, pencerenin ömrü boyunca, dışarıda lapa lapa yağan karısını izliyordu. Evin içi sıcacıktı ve mutfaktan mis gibi kurabiye kokuları yapılabilir. Tam o sırada Melis, bahçe kapısının yanındaki çöp kutusunun arkasında küçük bir karaltı fark etti.

Dikkatlice bakıldığında, tüyleri birbirine karışmış, zayıf ve gri renkli bir kedinin titrediğini gördü. Kedicik, soğuktan korunmak için küçük bir yumak haline gelmişti. Melis'in kalbi sızdı. "Anne, bak! Dışarıda çok soğuk bir kedi var" diye bağırdı. Annesi hemen yanına geldi. Birlikte kediyi korkutmadan yanlarına çağırmaya karar verdiler.

Annesi mutfaktan küçük bir kase ılık süt ve biraz anne diledi. Melis, kapının önünde eski bir hırkasını serdi. Kedicik önce uzaklaşarak yaklaştı, sonra karnı doyunca ve o sıcak hırkayı bulunca yumuşacık bir "Miyav" sesi çıkardı. Bu, bir imza şarkısıdır. Melis o an, bir canlıya yardım dünyanın en güzel duygusu olduğunu gösteriyor.

Kısa bir süre sonra kedinin sağlığı yerine geldi. Melis ona "Gümüş" adını koydu. Gümüş artık sadece bahçenin değil, ailenin bir parçası olmuştu. Melis her gün okulundan Gümüş onu kapıda karşılıyor, Melis de onun bakımını ihmal etmiyordu. Gümüş'ün mamasını vermesini ve tüylerini tarayarak Melis'e sorumluluk almayı öğretmişti.

Bir akşam babası, "Melis biliyor musun?" dedi. "Hayvanları seviyorlar, sadece onların yemek vermeleri mümkün değil. Bunların da bilinenleri anlaşılabiliyor ve yaşamlarına saygı duymaktır." Melis babasına hak verdi. Artık sokakta onu canlıya daha dikkatli arıyorlardı, onlar için kapının önünde bir kap su koymayı hiç unutmuyordu. Küçük bir kedinin hayatına dokunmak, Melis'in geniş kapsamlı bir sevgi ormanı büyümüştü."""},
        
        24: {"title": "24. Okuma Parçası: Sıddık ve Fındık", "content":"""Sıddık, her sabah olduğu gibi o gün de erkenden uyandı. Güneş, odasının perdelerinden süzülürken kapının tırmalanma sesini duydu. Bu ses, en yakın dostu Fındık’ın "Günaydın!" deme şekliydi. Fındık, tüyleri kahverengi, kulakları hafifçe düşük ve kuyruğu her zaman neşeyle sallanan bir köpekti.

Sıddık ve Fındık, birlikte büyümüşlerdi. Sıddık yürümeyi yeni öğrenirken Fındık onun yanında adım atar, Sıddık düştüğünde ise hemen yanına koşup yüzünü yalardı. Aralarındaki bağ, sadece bir sahiplik ilişkisi değil, derin bir dostluktu. Fındık, Sıddık’ın üzgün olduğunu sadece bakışlarından anlar, başını hemen Sıddık’ın dizine koyarak onu teselli etmeye çalışırdı.

Bir gün, Sıddık en sevdiği oyuncağını bahçede unuttu. Akşam bastırınca dışarıda şiddetli bir yağmur başladı. Sıddık oyuncağı için endişelenirken, Fındık çoktan harekete geçmişti. Yağmura ve çamura aldırmadan bahçeye fırladı. Islanmış ve titriyor olsa da oyuncağı ağzına alıp kapının önüne getirdi. Sıddık kapıyı açtığında karşısında sırılsıklam ama gururlu bir dost buldu. O an Sıddık, dostluğun sadece oyun oynamak değil, birbirini korumak ve kollamak olduğunu bir kez daha anladı.

Sıddık hemen bir havlu getirdi ve Fındık’ı özenle kuruladı. Ona en sevdiği mamadan verdi. Fındık, sıcak bir köşeye kıvrılıp uykuya dalarken, Sıddık da onun yanında oturup başını okşadı. Birlikte geçirdikleri her an, Sıddık’a sabırlı olmayı ve karşılık beklemeden sevmeyi öğretiyordu.

Yıllar geçse de bu dostluk hiç bozulmadı. Sıddık okuldan döndüğünde onu ilk karşılayan hep Fındık oldu. Çünkü biliyorlardı ki; gerçek bir dostunuz varsa, en yağmurlu günler bile güneşli bir bahar günü gibi sıcacıktır."""},
        
        25: {"title": "25. Okuma Parçası: Uyku Vakti Gelince", "content":"""Güneş yavaş yavaş dağların arkasına saklanmış, gökyüzü lacivert bir renge bürünmüştü. Sokak lambaları birer birer yanarken, küçük Defne için günün en zor anı gelmişti: Uyku vakti! Defne aslında uykuyu çok seviyordu ama oyun oynamayı ve masal dinlemeyi daha çok seviyordu. "Neden uyumalıyım ki?" diye sordu annesine.

Annesi, Defne’nin yanına oturdu ve yumuşak bir sesle anlatmaya başladı: "Biliyor musun Defne, uyku vakti geldiğinde sadece biz değil, bütün doğa dinlenmeye çekilir. Çiçekler yapraklarını kapatır, minik kuşlar yuvalarında birbirine sokulur. Uyku, vücudumuzun kendini yenilediği sihirli bir zamandır. Yarın daha hızlı koşabilmen ve daha yüksekten zıplayabilmen için pillerini doldurman gerekir."

Defne, pijama takımını giydi ve dişlerini özenle fırçaladı. Yatağına uzandığında yastığı bir bulut kadar yumuşaktı. Annesi ona en sevdiği masalı okumaya başladı. Masalda uçan filler, konuşan yıldızlar ve çikolatadan ağaçlar vardı. Defne gözlerini kapattığında, bu masal kahramanlarının rüyalarında onu beklediğini biliyordu.

Uyku sadece dinlenmek değildi, aynı zamanda yeni maceraların kapısıydı. Defne, rüyasında bulutların üzerinde zıplayabileceğini ve deniz kızlarıyla yüzebileceğini hayal etti. Odanın içindeki gece lambasının hafif ışığı, ona güven veriyordu. Yorganını burnuna kadar çekti ve derin bir nefes aldı.

Gece ilerledikçe Defne’nin nefesleri düzene girdi. Artık derin bir uykudaydı. O uyurken vücudu boyunu uzatıyor, zihni ise gün boyu öğrendiği bilgileri düzenli bir kütüphane gibi yerleştiriyordu. Sabah güneş odasına doğduğunda, Defne kendini bir kahraman kadar güçlü hissedecekti. Çünkü o, zamanında uyumanın ve güzel rüyalar görmenin sırrını artık biliyordu."""},
        
        26: {"title": "26. Okuma Parçası: Küçük Damlanın Büyük Yolculuğu", "content":"""Gökyüzünde, bembeyaz ve pamuk gibi bir bulutun üzerinde minicik bir su damlası yaşıyordu. Adı "Pırıl"dı. Pırıl, dünyadaki çok merak ediyor, oradaki çiçeklere ve çocuklara dokunmak istiyordu. Bir bahar sabahı, gök gürültülü bir davul gibi çalınca Pırıl, yöntemlerle birlikte el ele tutuşup buluttan aşağı doğru süzülmeye başladı. Bu, Pırıl'ın ilk dansıydı!

Pırıl, havada süzülürken rüzgarın ritmiyle sağa sola sallanıyor, bir balerin gibi dönüyordu. Önce bir çınar ağacının geniş yapraklarına kondu. Orada bir süre dinlendikten sonra kaydıraktan kayar gibi yaprağın ucunda yuvarlanıp susuz kaldı ve bir menekşenin kalbine düştü. Menekşe, Pırıl sayesinde canlandı ve yapraklarını neşeyle gökyüzüne açtı. Pırıl, bir canlıya hayat vermenin mutluluğuyla parlıyordu.

Daha sonra güneş bulutlarının çeşitleri görüldü. Hava ısınmaya başladığında Pırıl, kendini bir tüyü kadar hafif hisseder. Güneşin sıcaklığı onu kucakladı ve Pırıl, görünür kanatların var olduğu gibi yukarıdaya, gökyüzüne doğru yükselmeye başladı. "Gidiyorum ama yine yapabilirim!" diye fısıldadı.

Pırıl tekrar bulutuna ulaştığında, yaşadığı macerayı arkadaşlarına anlattı. O artık sadece bir su damlası değil, doğanın büyük kalıntılarının önemli bir parçasıydı. Yağmur olarak yağıyor, hava besleniyor, derelere karışıyor ve sonra buharlaşıp evde geri dönüyor.

O gün sonra çocukların gökyüzünden düşen yağmur damlalarını izlerken, onun birinin aslında birer "Pırıl" olduğu ve doğal olarak onun damlaya ihtiyacının bulunabildiğiler. Çünkü su varsa hayat vardı ve suyun bu bitmeyen dansı dünyada her zaman yemyeşil tutacaktı."""},
        
        27: {"title": "27. Okuma Parçası: Fırat'ın Sadık Dostu", "content":"""Fırat, uzun zamandır bir köpek sahibi olmanın hayalini kuruyordu. Sonunda doğum gününde babası ona sürpriz yaparak bembeyaz, tüyleri pamuk gibi yumuşacık bir yavru köpek getirdi. Fırat, yerinde duramayan bu sevimli köpeğe "Lokum" adını verdi. Çünkü o, gerçekten de tatlı bir şekerleme gibi görünüyordu.

Ancak bir köpek sahibi olmak, sadece onunla oyun oynamak demek değildi. Babası Fırat’ın karşısına geçip, "Bak Fırat," dedi. "Lokum artık bizim ailemizin bir üyesi. Onun karnını doyurmak, suyunu tazelemek ve her gün yürüyüşe çıkarmak senin görevin. Bir canlıya bakmak büyük bir sorumluluktur." Fırat gururla başını salladı. Artık o da bir "hayvan dostu" sorumluluğu taşıyordu.

İlk günler çok eğlenceli geçti. Fırat, bahçede Lokum’la top oynuyor, Lokum ise kuyruğunu neşeyle sallayarak Fırat’ın peşinden koşuyordu. Ama bir sabah dışarıda yağmur yağıyordu ve Fırat sıcacık yatağından çıkmak istemedi. Lokum ise kapının önünde bekliyor, dışarı çıkmak için sabırsızlanıyordu. Fırat bir an, "Bugünlük bir başkası çıkarsa ne olur ki?" diye düşündü.

Sonra Lokum’un kendisine güvenen o masum bakışlarını hatırladı. Babasının söyledikleri aklına geldi. Sorumluluk, sadece hava güzelken değil, her zaman sözünde durmaktı. Hemen yağmurluğunu giydi, Lokum’un tasmasını taktı ve birlikte bahçeye çıktılar. Yağmurun altında yürümek, çamurlu su birikintilerine basmak sandığından çok daha eğlenceliydi. Lokum, ıslanan tüylerini silkelediğinde ikisi de kahkahalarla güldüler.

O günden sonra Fırat ve Lokum hiç ayrılmadılar. Fırat, Lokum’un sadece sahibi değil, en yakın sırdaşı olmuştu. Lokum ona sadakati ve karşılıksız sevgiyi öğretirken; Fırat da bir canlıya emek vermenin, onu her koşulda korumanın ne kadar değerli olduğunu öğrendi. Lokum artık sadece bembeyaz bir köpek değil, Fırat’ın kalbindeki en büyük sevgi bağıydı."""},
        
        28: {"title": "28. Okuma Parçası: Küçük Dostların Koruyucusu: Ahmet", "content":"""Kış mevsimi gelmiş, soğuk rüzgarlar pencereleri titretmeye başlamıştı. Ahmet, odasının camından dışarıdaki ağaçların çıplak dallarına bakarken küçük bir kuşun titreyerek bir dala tutunmaya çalıştığını fark etti. Kuş o kadar minikti ki rüzgar estikçe havada savrulacak gibi oluyordu. Ahmet’in kalbi bu duruma çok üzüldü.

"Anne," diye seslendi. "Dışarıdaki kuşlar çok üşüyor ve muhtemelen çok açlar. Onlar için bir şeyler yapamaz mıyız?"

Annesi gülümseyerek Ahmet’in yanına geldi. "Tabii ki yapabiliriz oğlum. Hayvanlara yardım etmek en güzel erdemlerden biridir," dedi. Birlikte hemen işe koyuldular. Önce boş bir süt kutusunu temizleyip yanlarına pencereler açtılar. Ahmet, kutuyu renkli boyalarla süsledi; üzerine güneş ve çiçek resimleri çizdi. İçine bolca buğday ve ekmek kırıntısı doldurdular.

Ahmet, hazırladığı bu kuş yemliğini babasının yardımıyla bahçedeki büyük çınar ağacının en korunaklı dalına astı. Ayrıca ağacın dibine, donmayacak bir yere bir kap da taze su bıraktı. İlk başlarda kuşlar çekingendi, uzaktan izliyorlardı. Ancak Ahmet her sabah taze yem bırakmaya devam edince, kuşlar bu küçük kulübeye alışmaya başladılar.

Bir süre sonra bahçe, kuş cıvıltılarıyla şenlendi. Sadece serçeler değil, rengarenk sakalar ve meraklı sığırcıklar da misafirliğe geliyordu. Ahmet, her gün okuldan döndüğünde pencerenin kenarına oturup onları izlemeyi en sevdiği alışkanlığı haline getirdi. Onların karnının doyduğunu görmek, Ahmet'e büyük bir mutluluk veriyordu.

Zamanla Ahmet, sadece kendi bahçesindeki değil, mahalledeki diğer kuşları da düşünmeye başladı. Arkadaşlarına bu fikrini anlattı. Kısa sürede tüm arkadaşları evlerinin önüne benzer yemlikler hazırlayıp astılar. Ahmet sayesinde o kış, mahalledeki hiçbir kuş aç kalmadı. Küçük bir çocuğun merhameti, koca bir mahallenin sevgiyle dolmasını sağlamıştı."""},
        
        29: {"title": "29. Okuma Parçası: Yedi Taş", "content":"""Cumartesi öğleden sonraydı. Mahallenin çocukları top sahasının yanındaki boş alanda toplanmışlardı. Herkesin elinde tableti veya telefonu olduğu o günlerden biri değildi; bugün "eski usul" eğlenme günüydü. Elif, yerden seçtiği yassı taşları üst üste dizmeye başladı. Bir, iki, üç... Tam yedi tane yassı taş!

"Hadi arkadaşlar!" diye bağırdı Elif. "Yedi Taş oynamaya hazır mısınız?"

Hemen iki grup kurdular. Oyunun kuralı basitti ama büyük bir dikkat gerektiriyordu. Gruplardan biri, yumuşak bir topla üst üste dizilmiş taşları devirmeye çalışacak; diğer grup ise devrilen taşları ebe yakalanmadan tekrar üst üste dizmeye çalışacaktı. Heyecan doruktaydı. Arda, topu eline aldı, nişan aldı ve... "Güm!" Taşlar dört bir yana dağıldı.

Şimdi yarış başlamıştı! Bir grup kaçıyor, diğer grup topu kapıp onları "ebelemeye" çalışıyordu. Elif ve arkadaşları, top kendilerine değmeden hızlıca taşların yanına koşup birer birer taşları dizmeye başladılar. Bu sadece bir oyun değil, müthiş bir iş birliğiydi. Biri arkadaşını uyarıyor, diğeri topu takip ediyor, bir diğeri ise en doğru taşı en alta koymak için çabalıyordu.

Oyun sırasında küçük bir tartışma çıktı; acaba top Can’a değmiş miydi? Can, "Evet, top ayağıma hafifçe değdi," diyerek dürüstçe ebelendiğini kabul etti. Arkadaşları onu bu dürüstlüğünden dolayı alkışladılar. Çünkü oyunda kazanmaktan daha önemli olan şey dürüst kalmaktı.

Güneş batarken herkes kan ter içinde kalmış ama yüzlerine kocaman bir gülümseme yerleşmişti. Yedi taşın etrafında kurulan bu dostluk, ekran başındaki oyunlardan çok daha gerçekti. Elif taşları cebine koyarken, "Haftaya yine buradayız!" dedi. Çocuklar evlerine dönerken, geleneksel bir oyunu yaşatmanın ve birlikte hareket etmenin mutluluğunu yaşıyorlardı."""},
        
        30: {"title": "30. Okuma Parçası: Bir Avuç Paylaşım: Unun Var Mı?", "content":"""Sıcak bir yaz ikindisiydi. Zehra Hanım, mutfakta ailesi için en sevdikleri elmalı keki yapmaya karar vermişti. Elmaları rendeledi, tarçını hazırladı, yumurtaları çırptı. Tam unu ekleyeceği sırada kavanozun boş olduğunu fark etti. Eyvah! Kekin en önemli malzemesi eksikti ve markete gidecek kadar vakti yoktu.

Zehra Hanım’ın kızı Pelin, annesinin üzüldüğünü görünce, "Anneciğim, neden yan komşumuz Hatice Teyze’ye sormuyoruz? Annem her zaman 'Komşu komşunun külüne muhtaçtır' derdi," dedi. Pelin, annesinden izin alarak eline boş bir kase aldı ve alt kata, Hatice Teyze’nin kapısına gitti.

Kapıyı güler yüzle açan Hatice Teyze, Pelin’i dinledikten sonra içeriye süzüldü. Az sonra elinde ağzına kadar un dolu bir kaseyle döndü. "Tabii ki var kızım, paylaşmak ne güzeldir," dedi. Pelin teşekkür ederek koşa koşa eve döndü. Kek fırına verildi ve kısa süre sonra bütün apartmanı mis gibi bir koku sardı.

Kek piştiğinde Zehra Hanım, en büyük dilimi bir tabağa koydu. Üzerine biraz pudra şekeri serpti. Pelin’e dönerek, "Haydi bakalım Pelin, şimdi bu keki Hatice Teyze’ne götür. Paylaşılan un, paylaşılan bir keke dönüşmeli," dedi.

Pelin tabağı götürdüğünde Hatice Teyze çok mutlu oldu. Sadece bir kase un istemekle başlayan bu olay, güzel bir sohbete ve sıcacık bir teşekküre dönüşmüştü. O akşam Pelin, yardımlaşmanın sadece eksik bir malzemeyi tamamlamak olmadığını; aslında insanlar arasındaki sevgi bağını güçlendirdiğini anladı. Küçük bir kase un, koca bir mahalle dolusu mutluluğa kapı aralamıştı. Pelin artık biliyordu ki; ihtiyacımız olduğunda bir kapıyı çalmak cesaret, o kapıyı açana teşekkür etmek ise en büyük nezaketti."""},
        
        31: {"title": "31. Okuma Parçası: Kalbin Ritmiyle Dans", "content":"""Deniz, müziği çok seven ama topluluk önünde hareket etmekten biraz çekinen bir çocuktu. Okulda yapılacak olan "Bahar Şenliği" için her sınıfın bir gösteri hazırlaması gerekiyordu. Deniz’in sınıfı ise o yıl "Dünya Dansları" temasını seçmişti. Öğretmenleri sınıfa gelip, "Çocuklar, dans etmek sadece adımları ezberlemek değildir; duygularımızı vücudumuzla anlatmaktır," dediğinde Deniz derin bir nefes aldı.

İlk provalar başladığında Deniz, ayaklarının birbirine dolanacağını düşünüyordu. Ancak müzik çalmaya başladığında işler değişti. Davulun sesi kalbinin atışı gibiydi; flütün ezgisi ise rüzgarda uçuşan bir yaprağı andırıyordu. Öğretmeni Deniz’in yanına gelip fısıldadı: "Müziği sadece kulağınla değil, kalbinle dinle Deniz. O zaman vücudun ne yapacağını kendiliğinden bilecektir."

Deniz gözlerini kapattı. Önce parmak uçları kıpırdadı, sonra omuzları ritme eşlik etti. Arkadaşlarıyla el ele tutuşup büyük bir halka oluşturduklarında, artık sadece kendi dansını değil, arkadaşlığın gücünü de hissediyordu. Birlikte zıplıyor, birlikte dönüyor ve aynı anda alkış tutuyorlardı. Hata yapsalar bile birbirlerine gülümseyerek devam ediyorlardı. Çünkü bu bir yarışma değil, bir kutlamaydı.

Şenlik günü geldiğinde Deniz, sahne ışıklarının altında yerini aldı. Sahnenin karşısında oturan ailesini ve arkadaşlarını gördüğünde kalbi heyecandan "küt küt" atıyordu. Müzik başladığı an tüm korkuları uçup gitti. Deniz artık sadece dans ediyordu. Kolları gökyüzüne uzanan bir ağaç gibi özgür, adımları ise nehirdeki su damlaları kadar akıcıydı.

Gösteri bittiğinde alkış sesleri tüm bahçeyi doldurdu. Deniz o gün önemli bir şey fark etti: Dans etmek sadece eğlenceli bir spor değil, aynı zamanda insanın içindeki neşeyi dünyayla paylaşma biçimiydi. Artık müzik duyduğu her yerde, adımları neşeyle dansa eşlik etmeye hazırdı."""},
        
        32: {"title": "32. Okuma Parçası: Gökyüzünden Gelen Dost: Aydede", "content":"""Ege, gökyüzünü ve yıldızları izlemeyi çok seven meraklı bir çocuktu. Geceleri penceresinin kenarına oturur, Ay’ın şekillerini defterine çizerdi. Ancak Ege’nin bir başka hayali daha vardı: Kendisine eşlik edecek, birlikte maceralara koşacağı sadık bir dost.

Bir akşamüzeri, babası eve elinde küçük bir sepetle geldi. Sepetin içinden, tüyleri bembeyaz, alnında ise tıpkı hilale benzeyen sarı bir lekesi olan minik bir köpek çıktı. Ege, köpeği görür görmez "Aydede!" diye bağırdı. "Alnındaki o işaret tıpkı Ay’a benziyor, senin adın bundan sonra Aydede olsun."

Aydede ve Ege kısa sürede ayrılmaz bir ikili oldular. Aydede sıradan bir köpek değildi; sanki Ege’nin ne hissettiğini hemen anlıyordu. Ege ödev yaparken masanın altında sessizce bekliyor, Ege üzüldüğünde ise gelip başını dizine koyuyordu. Ancak Aydede’nin en sevdiği vakit, bahçede oynadıkları saklambaç oyunuydu. Aydede o kadar akıllıydı ki, Ege nereye saklanırsa saklansın, burnuyla havayı koklar ve neşeyle havlayarak onu hemen bulurdu.

Bir gün parkta oynarken Ege’nin en sevdiği mavi şapkası rüzgârla birlikte yüksek bir çalılığın arkasına uçtu. Çalılıklar çok dikenliydi ve Ege şapkasına ulaşamıyordu. Aydede hemen durumu fark etti. Küçük boyuyla dikenlerin arasından ustalıkla geçti ve şapkayı ağzıyla kavrayıp geri getirdi. Ege, dostuna sıkıca sarıldı. "Teşekkür ederim Aydede, sen sadece bir oyun arkadaşı değil, harika bir yardımcısın," dedi.

O gece Ege yine pencereden gökyüzüne baktı. Gökteki Ay ışıl ışıl parlıyordu, yanında ise mışıl mışıl uyuyan kendi "Aydede"si vardı. Ege o an anladı ki; bir dostun sevgisi, dünyadaki tüm yıldızlardan daha parlaktı. Bir canlıya emek vermek ve onun sevgisini kazanmak, Ege’nin hayatına kocaman bir ışık katmıştı. Artık geceleri sadece Ay’ı değil, yanındaki sadık dostunu da sevgiyle izliyordu."""},
        
        33: {"title": "33. Okuma Parçası: Canım Bursa", "content":"""Ali, o sabah heyecanla uyandı. Bugün sınıf arkadaşlarına memleketi olan Bursa'yı anlatacaktı. Akşamdan hazırladığı notları eline aldı ve pencereden dışarı, şehrin simgesi olan Uludağ’a baktı. Dağın tepesindeki beyaz karlar, şehre bir taç gibi yakışıyordu.

Okula gittiğinde kürsüye çıktı ve anlatmaya başladı: "Arkadaşlar, bugün size 'Yeşil Bursa'yı anlatacağım. Bursa denince akla sadece yeşil ağaçlar değil, tarih kokan sokaklar gelir." Ali, çantasından bir İpekböceği kozası çıkardı. Bursa’nın meşhur ipek kumaşlarının nasıl yapıldığını, bu küçücük canlıların ne kadar büyük bir emeği olduğunu anlattı.

Sözlerine şehrin merkezindeki heybetli yapılarla devam etti. "Ulu Cami’nin yirmi kubbesini ve içerisindeki şırıl şırıl akan şadırvanı görmelisiniz. Orada insanın içi huzurla dolar," dedi. Ardından herkesin çok sevdiği Karagöz ve Hacivat’tan bahsetti. Bursa’nın bu iki komik kahramanı, yüzyıllardır insanları hem güldürüyor hem de düşündürüyordu.

"Peki ya yemekler?" diye sordu sınıftan bir arkadaşı. Ali gülümseyerek cevap verdi: "Bursa denince akla hemen mis gibi İskender kebap ve üzerine dökülen sıcak tereyağı gelir. Tatlı olarak ise meşhur kestane şekerini yemeden dönmemelisiniz."

Ali, konuşmasını bitirirken Bursa’nın sadece bir şehir değil, bir Osmanlı başkenti ve yaşayan bir tarih olduğunu vurguladı. İznik’in masmavi çinilerinden, Cumalıkızık’ın daracık taş sokaklarından bahsetti. Arkadaşları Ali’yi alkışlarken, herkesin içinde bu güzel şehri ziyaret etme isteği uyanmıştı.

Ali o gün şunu anladı: Memleketini tanımak ve onu başkalarına anlatmak, bir hazineyi paylaşmak gibiydi. Bursa; doğasıyla, tarihiyle ve lezzetleriyle Ali’nin kalbinde her zaman en özel yerinde kalacaktı."""},
       
        34: {"title": "34. Okuma Parçası: Tellerin Melodisi", "content":"""Mert, o sabah erkenden uyandı. Bugün hayatındaki en heyecanlı günlerden biriydi; çünkü ilk gitar dersine gidecekti. Odasının köşesinde duran, babasının doğum günü hediyesi olan parlak kahverengi gitarına baktı. Tellerine dokunduğunda çıkan ses şimdilik sadece bir gürültü gibiydi ama Mert, o tellerden harika şarkılar çıkaracağı günün hayalini kuruyordu.

Kurs merkezine girdiğinde içeriden gelen piyano ve keman sesleri onu karşıladı. Gitar öğretmeni Murat Bey, Mert’i gülümseyerek içeri davet etti. "Hoş geldin Mert," dedi. "Müzik, sabırla örülen bir yolculuktur. Bugün ilk adımımızı atıyoruz."

Murat Bey, Mert’e gitarı nasıl tutması gerektiğini ve tellere nasıl nazikçe dokunacağını gösterdi. İlk başta Mert'in parmakları tellere basarken biraz zorlandı. Notları sırasıyla çalmak sandığı kadar kolay değildi. Bir ara içinden, "Acaba hiç öğrenemeyecek miyim?" diye geçirdi. Parmak uçları biraz sızlıyor, istediği o temiz sesi bir türlü çıkaramıyordu.

Öğretmeni, Mert'in yüzündeki endişeyi fark etti. "Bak Mert," dedi, "En ünlü müzisyenler bile ilk günlerinde senin gibi hissettiler. Önemli olan parmaklarının değil, kalbinin pes etmemesidir. Küçük adımlarla, her gün çalışarak o teller senin en yakın arkadaşın olacak."

Mert o gün dersten çıktığında cebinde sadece nota kağıtları yoktu; aynı zamanda büyük bir azim vardı. Eve gider gitmez gitarını kucağına aldı. Öğrendiği ilk basit melodiyi tekrar tekrar çalıştı. Birinci gün zordu, ikinci gün biraz daha kolaylaştı. Bir haftanın sonunda, o "gürültü" dediği sesler artık minik bir şarkıya dönüşmüştü.

Annesi ve babası Mert’in çaldığı ilk parçayı alkışlarken, Mert başarmanın mutluluğunu yaşıyordu. Müzik ona sadece notaları değil; pes etmemeyi, disiplinli olmayı ve emeğin ne kadar değerli olduğunu öğretmişti. Artık her akşam gitarının tellerine dokunduğunda, parmaklarından dökülen melodiler sadece odasını değil, hayallerini de renklendiriyordu."""},
       
        35: {"title": "35. Okuma Parçası: Yankılı Mağara", "content":"""Eren ve küçük kardeşi İpek, hafta sonu tatilinde dedelerinin köyüne gitmişlerdi. Köyün hemen arkasındaki tepede, ağaçların arasına gizlenmiş karanlık bir mağara girişi vardı. Köylüler oraya "Yankılı Mağara" derlerdi. İpek, mağaranın önünden her geçişlerinde merakla içeri bakıyor ama karanlıktan biraz çekiniyordu. "Sence içeride devler mi yaşıyor, yoksa saklı hazineler mi var?" diye sordu ağabeyine.

Eren, "Hadi gel, birlikte keşfedelim," dedi. Yanlarına küçük birer el feneri aldılar ve mağaranın ağzına kadar yürüdüler. İçerisi dışarıya göre çok daha serindi. İlk adımlarını attıklarında fenerin ışığı duvarlarda dans etmeye başladı. Mağaranın tavanından aşağıya doğru uzanan garip şekilli kayalar vardı. Eren, "Bunlara sarkıt denir," diye açıkladı. "Yerden yukarı doğru yükselenlere ise dikit denir. Doğanın binlerce yılda yaptığı heykeller bunlar."

İlerledikçe bir su sesi duydular. Mağaranın derinliklerinde küçük bir yeraltı pınarı akıyordu. Işıkları suyun üzerine düştüğünde, suyun içindeki minik çakıl taşları mücevher gibi parladı. İpek’in korkusu gitmiş, yerini büyük bir hayranlığa bırakmıştı. Tam o sırada başlarının üzerinde bir kanat çırpış sesi duyuldu. Feneri yukarı çevirdiklerinde, tavana asılı duran küçük bir yarasayı fark ettiler. Eren, yarasaların gündüzleri burada dinlendiğini ve aslında çok faydalı hayvanlar olduklarını anlattı.

Mağaranın içindeki yankı ise en eğlenceli kısımdı. İpek, "Merhaba!" diye bağırdı. Duvarlar ona "Merhaba... Merhaba..." diye cevap verdi. Çocuklar, doğanın bu gizli dünyasında aslında korkulacak hiçbir şey olmadığını, her köşede keşfedilmeyi bekleyen bir mucize olduğunu anladılar.

Dışarı çıktıklarında güneş hala parlıyordu. İpek, mağaranın içinde ne dev ne de altın bulmuştu ama hayal gücünden çok daha değerli bir şey kazanmıştı: Bilgi ve macera duygusu. O akşam dedelerine mağaradaki sarkıtları ve yankıları anlatırken, bir sonraki keşifleri için şimdiden plan yapmaya başlamışlardı."""},
       
        36: {"title": "36. Okuma Parçası: Leyla'nın Resmi", "content":"""Leyla, bembeyaz bir kağıdın önünde oturduğunda kendini dünyanın en güçlü büyücüsü gibi hissederdi. Onun asası, ucu hafifçe aşınmış kurşun kalemi; iksirleri ise gökkuşağının tüm renklerini barındıran boya kutusuydu. Çevresindeki herkes dünyayı olduğu gibi görürken, Leyla dünyayı olması gerektiği gibi hayal ederdi.

Bir gün sınıfta öğretmenleri "En sevdiğiniz yeri çizin," dediğinde arkadaşları parkları, evlerini ya da okul bahçesini çizmeye başladılar. Leyla ise gözlerini kapattı. Zihninde mor yapraklı ağaçların olduğu, nehirlerinden portakal suyu akan ve bulutların pamuk şekerden yapıldığı bir diyar canlandı. Fırçasını eline aldı ve büyük bir heyecanla çalışmaya başladı.

Maviye boyadığı gökyüzüne pembe noktalar ekledi. "Bunlar şarkı söyleyen yıldızlar," dedi kendi kendine. Yeşili sadece çimenler için değil, gökyüzünde uçan devasa kuşlar için kullandı. Leyla resim yaparken zamanın nasıl geçtiğini anlamıyordu. Onun için her renk bir duyguydu; sarı neşeyi, turuncu enerjiyi, mavi ise huzuru temsil ediyordu. "Leyla'nın Renkli Dünyası" metnini temel alarak; hayal gücü, sanatın iyileştirici gücü, renklerin anlamları ve özgüven temalarını işleyen, ilkokul seviyesine uygun özgün metni aşağıda bulabilirsiniz.

Leyla’nın Renkli Dünyası
Leyla, bembeyaz bir kağıdın önünde oturduğunda kendini dünyanın en güçlü büyücüsü gibi hissederdi. Onun asası, ucu hafifçe aşınmış kurşun kalemi; iksirleri ise gökkuşağının tüm renklerini barındıran boya kutusuydu. Çevresindeki herkes dünyayı olduğu gibi görürken, Leyla dünyayı olması gerektiği gibi hayal ederdi.

Bir gün sınıfta öğretmenleri "En sevdiğiniz yeri çizin," dediğinde arkadaşları parkları, evlerini ya da okul bahçesini çizmeye başladılar. Leyla ise gözlerini kapattı. Zihninde mor yapraklı ağaçların olduğu, nehirlerinden portakal suyu akan ve bulutların pamuk şekerden yapıldığı bir diyar canlandı. Fırçasını eline aldı ve büyük bir heyecanla çalışmaya başladı.

Maviye boyadığı gökyüzüne pembe noktalar ekledi. "Bunlar şarkı söyleyen yıldızlar," dedi kendi kendine. Yeşili sadece çimenler için değil, gökyüzünde uçan devasa kuşlar için kullandı. Leyla resim yaparken zamanın nasıl geçtiğini anlamıyordu. Onun için her renk bir duyguydu; sarı neşeyi, turuncu enerjiyi, mavi ise huzuru temsil ediyordu. 

Resmi bittiğinde arkadaşları masasının etrafına toplandı. Bazıları şaşkınlıkla bakıyordu. "Leyla, mor yapraklı ağaç olur mu hiç?" diye sordu biri. Leyla gülümseyerek cevap verdi: "Benim dünyamda her şey mümkün. Eğer hayal edebiliyorsak, o şey gerçektir." Öğretmeni Leyla’nın yanına gelip resme uzun uzun baktı. "Harika bir hayal gücün var Leyla. Sanat, dünyayı sadece gözlerimizle değil, kalbimizle de görmemizi sağlar," dedi.

O günden sonra Leyla, sadece kağıtları değil, çevresindeki her şeyi renklendirmeye karar verdi. Gri bir kaldırım taşını boyalı parmaklarıyla hayali bir çiçeğe dönüştürdü, eski bir ayakkabı kutusundan rengarenk bir kuş yuvası yaptı. Leyla’nın renkli dünyası, sadece onun zihninde kalmamış, dokunduğu her yere neşe saçmaya başlamıştı. Çünkü o biliyordu ki; hayallerine renk veren bir çocuk, dünyayı daha güzel bir yer haline getirebilirdi."""},
       
        37: {"title": "37. Okuma Parçası: Mozaik", "content":"""Okulun bahçesindeki eski duvarın onarılması gerekiyordu. Öğretmenimiz elinde kocaman bir kutuyla sınıfa girdi. Kutunun içinde rengarenk, küçük, kare şeklinde taşlar vardı. "Çocuklar," dedi öğretmenimiz, "bugün hep birlikte bir mozaik tablosu yapacağız. Unutmayın, mozaik yapmak sabır ve dikkat isteyen bir sanattır."

Önce hepimiz şaşırdık. Bu minicik taşlar nasıl olur da güzel bir resim oluşturabilirdi ki? Her birimiz avucumuza farklı renklerde taşlar aldık. Kırmızı, masmavi, parlak sarı ve yeşil taşlar... Öğretmenimiz yere büyük bir taslak çizdi. Bu, kanatlarını açmış kocaman bir kuş resmiydi.

Sırayla taşları yerleştirmeye başladık. İlk başta sadece karışık renkli taşlar gibi görünüyordu. Ancak taşlar yan yana geldikçe büyüleyici bir şeyler olmaya başladı. Mavi taşlar kuşun gövdesini, sarı taşlar ise parlayan gözlerini oluşturuyordu. Bir taşı yanlış yere koysak, bütün desen bozulabiliyordu. Bu yüzden birbirimize yardım ederek, hangi taşın nereye daha çok yakışacağını tartıştık.

Öğretmenimiz bize eski zamanlarda insanların bu sanatı sarayları ve şehirleri süslemek için kullandığını anlattı. "Mozaik, tıpkı bizim sınıfımız gibidir," dedi. "Her biriniz farklı bir renksiniz, farklı özellikleriniz var. Ama bir araya geldiğinizde, işte böyle muhteşem bir bütün oluşturuyorsunuz."

Akşam olduğunda duvarın üzerindeki kuş, batan güneşin ışıklarıyla parlıyordu. Uzaktan bakınca taşların arasındaki çizgiler kayboluyor, sanki kuş her an havalanıp uçacakmış gibi duruyordu. O gün sadece bir resim yapmamıştık; küçük parçaların birleşerek nasıl büyük bir güç ve güzellik oluşturduğunu öğrenmiştik. Artık ne zaman bir mozaik görsek, o küçük taşların sabırla dizilişindeki emeği ve aralarındaki o sessiz uyumu hatırlayacaktık."""},
        
        38: {"title": "38. Okuma Parçası: Gökyüzündeki Takipçi: Ay Peşimi Bırakmıyor", "content":"""O akşam Berk ve ailesi, şehirden uzaktaki dedesinin köyüne gitmek için yola çıkmışlardı. Araba yavaşça virajlı yollarda ilerlerken Berk, başını camın kenarına yaslayıp gökyüzünü izlemeye başladı. Gökyüzü o gece o kadar berraktı ki yıldızlar sanki birer elmas gibi parlıyordu. Ama Berk’in dikkatini çeken başka bir şey vardı: Ay!

"Baba," diye seslendi Berk heyecanla. "Ay bizimle geliyor! Bak, ben ne kadar hızlı gidersem o da o kadar hızlı koşuyor. Az önce ağacın arkasındaydı, şimdi tepenin üzerine geçti. Neden peşimizi bırakmıyor?"

Babası dikiz aynasından Berk’e gülümseyerek baktı. "Bu çok güzel bir gözlem Berk. Ay gerçekten de bizi takip ediyor gibi görünüyor, değil mi? Ama aslında Ay, bizden o kadar uzakta ki biz hareket ettikçe onun açısı neredeyse hiç değişmiyor. Bu yüzden çevremizdeki ağaçlar ve evler hızla geride kalırken, Ay sanki hep aynı noktada duruyormuş ve bizimle geliyormuş gibi hissediyoruz."

Berk bir süre sessizce düşündü. Bu tıpkı bir illüzyon gibiydi. Araba durduğunda Ay da duruyor, araba hızlandığında o da gökyüzünde süzülüyordu. Berk, "Peki, o zaman Ay herkese aynı anda mı eşlik ediyor?" diye sordu. Annesi araya girerek, "Evet tatlım," dedi. "Şu an yolda olan tüm çocuklar Ay'ın kendi peşlerinden geldiğini sanıyor. Ay, gökyüzündeki kocaman ve sadık bir fener gibi hepimizi aynı anda aydınlatıyor."

Köy evine vardıklarında Berk, arabadan inip gökyüzüne tekrar baktı. Ay, şimdi evin çatısının tam üzerindeydi. Berk ona el salladı ve fısıldadı: "Tamam, anladım. Sen bizi takip etmiyorsun, sen sadece bize yol gösteriyorsun." O gece Berk, bilimin ve doğanın harikalarını düşünerek huzurla uykuya daldı. Gökyüzündeki sadık dostu, penceresinden içeriye gümüşten bir ışık süzerek onu izlemeye devam ediyordu."""},
       
        39: {"title": "39. Okuma Parçası: Nerede Uyusam Acaba?", "content":"""Ormanın en meraklı üyesi olan küçük Tavşan Zıpzıp, o akşam yatağını biraz sıkıcı bulmuştu. "Her gün aynı yuvada uyumak ne kadar sıradan," diye düşündü. "Belki de başka hayvanların yatakları daha konforludur." Böylece Zıpzıp, kendine yeni bir uyku yeri bulmak için ormanda küçük bir yolculuğa çıktı.

İlk olarak yaşlı meşe ağacının altındaki bir kovuğa rastladı. İçerisi yumuşacık tüyler ve yapraklarla doluydu. "Tam bana göre!" diyerek içeri kıvrıldı. Ancak tam gözlerini kapatmıştı ki "Tık tık tık!" sesiyle irkildi. Sincap Çevik, kollarında meşe palamutlarıyla çıkageldi. "Burası benim kışlık depom ve yatağım Zıpzıp, burada zıplayamazsın!" dedi. Zıpzıp özür dileyerek oradan ayrıldı.

Sonra göl kenarındaki sazlıkların arasına gitti. Ördeklerin suyun üzerinde nasıl huzurla uyuduğunu gördü. O da ayaklarını suya soktu ama "Vırak!" diye bir ses duyuldu. Bir kurbağa, "Dikkat et Zıpzıp, burası biraz ıslaktır, senin tüylerin hemen ağırlaşır!" diye uyardı. Zıpzıp, suyun bir tavşan için pek de iyi bir yatak olmadığını anladı.

Yoluna devam ederken yüksek kayalıkların arasındaki bir mağara girişi gördü. "Burası çok geniş ve serin," dedi. Ama içeriden gelen derin bir horlama sesi yerdeki taşları bile titretiyordu. Koca Ayı uykusundaydı! Zıpzıp, bu kadar gürültülü bir yerde uyuyamayacağını fark edip sessizce uzaklaştı.

Güneş batıp yıldızlar çıkınca Zıpzıp iyice yorulmuştu. Ayakları onu kendiliğinden çalılıkların altındaki kendi yuvasına götürdü. İçeri girdiğinde toprağın o tanıdık kokusunu ve kuru otların yumuşaklığını hissetti. Kendi yuvası ne çok gürültülü ne çok ıslak ne de çok kalabalıktı. Zıpzıp, "En güzel yatak, insanın kendini en güvende hissettiği yerdir," diye fısıldadı. Kendi sıcak yuvasına kıvrıldı ve o gece hayatındaki en derin uykusuna daldı."""},
        
        40: {"title": "40. Okuma Parçası: Benimle Oynar Mısın?", "content":"""Okul bahçesi her zamanki gibi cıvıl cıvıldı. Bir gruptaki çocuklar saklambaç oynuyor, diğerleri ise basketbol potasının altında heyecanla zıplıyordu. Selim, okulun bahçesindeki büyük çınar ağacının gölgesinde tek başına oturuyordu. Elinde küçük, mavi bir kamyon vardı ve onu toprağın üzerinde yavaşça sürüyordu. İçten içe diğer çocukların yanına gitmek istiyor ama "Acaba beni aralarına alırlar mı?" diye düşünmekten çekiniyordu.

Tam o sırada, sınıftan arkadaşı Caner elinde bir topla Selim’in yanına yaklaştı. Caner, Selim’in yalnız başına kamyonuyla oynadığını görünce duraksadı. Selim, başını kaldırıp çekingen bir şekilde Caner’e baktı. Caner gülümseyerek, "Selim, kamyonun çok hızlı görünüyor! Benim topumla beraber bir yolculuğa çıkmaya ne dersin?" diye sordu.

Selim’in gözleri parladı. Beklediği o sihirli cümle gelmişti: "Benimle oynar mısın?"

Hemen ayağa kalktı ve "Tabii ki! Kamyonum topu taşıyabilir, böylece uzak diyarlara gidebiliriz," dedi. İki arkadaş, bahçenin bir köşesinde kendilerine küçük bir oyun alanı kurdular. Top, bazen kamyonun arkasındaki bir yolcu oldu, bazen de aşmaları gereken dev bir kaya. Onların neşeli seslerini duyan diğer çocuklar da merakla yanlarına geldi. "Biz de katılabilir miyiz?" diye sordular.

O gün okul bahçesinde sadece bir oyun kurulmadı, aynı zamanda yeni dostlukların temeli atıldı. Selim artık tek başına değildi. Birine oyun teklif etmenin ya da çekinen birini oyuna davet etmenin ne kadar değerli olduğunu anlamıştı. Oyun bitip zil çaldığında, Selim arkadaşlarına teşekkür etti. Bazen en büyük mutluluklar, sadece bir soru sormakla başlardı. Eve dönerken Selim'in aklında tek bir düşünce vardı: Yarın teneffüste kime "Benimle oynar mısın?" diye soracaktı?"""},
       
        41: {"title": "41. Okuma Parçası: Yemyeşil Şehir: Rize", "content":"""Dursun, o sabah penceresini açtığında dışarıda bembeyaz bir manzara vardı. Ama bu kar değildi; dağların yamacına bir yorgan gibi serilen sis bulutlarıydı. Dursun, "Bugün yine bulutların üzerinde uyandık!" diyerek neşeyle kahvaltıya koştu. Bugün okulda, yaşadığı şehir olan Rize’yi tanıtacaktı.

Okula gittiğinde tahtaya büyük bir çay yaprağı resmi çizdi. "Arkadaşlar," dedi. "Rize demek, huzur veren bir yeşillik demektir. Bizim burada dağlar denize o kadar yakındır ki her sabah dalga sesleriyle uyanır, çay kokusuyla kendimize geliriz." Çantasından küçük bir paket çay çıkardı ve arkadaşlarına koklattı. "Biliyor musunuz? İçtiğiniz o sıcacık çayların çoğu, bizim dik yamaçlarımızdaki bahçelerden toplanıyor. Çay toplamak sabır ister ama tadı tüm yorgunluğu unutturur."

Dursun, konuşmasına Rize’nin yaylalarıyla devam etti. Ayder Yaylası’nın gürül gürül akan şelalelerini, Kaçkar Dağları’nın zirvesindeki buz gibi gölleri anlattı. "Rize’de sadece yeşil yok, aynı zamanda köprülerin de hikayesi var," diyerek Fırtına Deresi üzerindeki taş kemer köprülerden bahsetti. Bu köprülerin yüzlerce yıldır azgın sulara nasıl direndiğini anlattığında herkes hayranlıkla onu dinliyordu.

Söz yemeklere gelince Dursun’un gözleri parladı. "Hamsili pilavımızı, mısır ekmeğimizi ve uzadıkça uzayan o meşhur muhlamamızı yemeden Rize’yi tanımış sayılmazsınız!" dedi. Sınıftaki arkadaşları muhlamanın peynirinin nasıl uzadığını hayal ederken Dursun, Karadeniz’in hareketli müziği olan tulum ve kemençeden de bahsetti. "Rize’de horon tepmek, rüzgarla dans etmek gibidir," diyerek sözlerini bitirdi.

O gün sınıfındaki herkes, Rize’nin sadece yağmuruyla değil, insanının sıcaklığı ve doğasının mucizeleriyle de çok özel bir yer olduğunu anladı. Dursun, bu güzel şehrin bir parçası olduğu için kendini çok şanslı hissediyordu."""},
      
        42: {"title": "42. Okuma Parçası: Sonbahar Yağmuru", "content":"""Sonbahar gelmiş, ağaçlar sarı ve turuncu kıyafetlerini giymişti. Küçük Nil, pencerenin kenarında oturmuş, gökyüzündeki gri bulutların toplanmasını izliyordu. Tam o sırada ilk yağmur damlası pıt diye cama vurdu. Nil’in gözleri neşeyle parladı çünkü dolabında giyilmeyi bekleyen en sevdiği eşyası oradaydı: Parlak, sarı lastik çizmeleri!

Annesinden izin alan Nil, sarı çizmelerini ayağına geçirdi, renkli şemsiyesini yanına aldı ve dışarı fırladı. Sokaklar mis gibi toprak kokuyordu. Nil için yağmur sadece su demek değildi; o, su birikintilerinde zıplamak, her damlada yeni bir oyun bulmak demekti. "Lık lık!" diye ses çıkaran bir su birikintisinin tam ortasına zıpladı. Çizmeleri sayesinde ayakları kupkuruydu ama etrafa saçılan su damlaları birer elmas gibi parlıyordu.

Yolda arkadaşı Mert’e rastladı. Mert’in ise kırmızı çizmeleri vardı. İki arkadaş, birikintilerin etrafında el ele tutuşup dönmeye başladılar. Nil, "Bak Mert!" dedi. "Sarı ve kırmızı çizmelerimiz yan yana gelince sanki sokakta bir gökkuşağı yürüyor gibi oluyor." Yağmur damlaları şemsiyelerine vurdukça çıkan "tıp tıp" seslerine, çocukların kahkahaları eşlik ediyordu.

Bir süre sonra yağmur dindi ve bulutların arasından utangaç bir güneş gülümsedi. Nil, çizmeleriyle ıslak yaprakların üzerinde yürürken doğanın nasıl tazelendiğini fark etti. Susuz kalmış minik çiçekler başlarını kaldırmış, tozlu yapraklar tertemiz olmuştu.

Eve döndüğünde Nil, çizmelerini kapının önüne özenle bıraktı. Onlar sadece birer ayakkabı değil, Nil’i doğayla buluşturan sihirli araçlardı. Nil o gün şunu anladı: Doğru kıyafetler ve neşeli bir kalple, en gri gün bile gökkuşağı kadar renkli geçebilirdi. Akşam yatağına yattığında, bir sonraki yağmuru ve sarı çizmeleriyle yapacağı yeni keşifleri hayal ederek uykuya daldı."""},
      
        43: {"title": "43. Okuma Parçası: Rüzgar Esince Neler Olur?", "content":"""O sabah, perdeler hafifçe havalandı ve odanın içine taze bir çiçek kokusu doldu. Sinan, pencereye koşup dışarı baktı. Dışarıda görünmez bir el, ağaçların dallarını nazikçe sallıyor, kurumuş yaprakları havada birer dansçı gibi döndürüyordu. "Rüzgâr gelmiş!" diye bağırdı.

Rüzgâr çok garip bir arkadaştı. Onu göremiyordunuz ama dokunuşunu yüzünüzde hissedebiliyor, sesini ağaçların hışırtısında duyabiliyordunuz. Sinan, bahçeye çıkınca rüzgârın neler yapabildiğini daha yakından izlemeye başladı. Bahçedeki rüzgâr gülü hızla dönmeye başlamıştı. Renkli kanatları o kadar süratli dönüyordu ki bir süre sonra renkler birbirine karıştı.

"Baba," dedi Sinan, "Rüzgâr bu kadar gücü nereden buluyor?"

Babası, Sinan’ın yanına gelerek gökyüzündeki rüzgâr türbinlerini işaret etti. "Bak Sinan, rüzgâr sadece yaprakları uçurmaz; o büyük kanatları döndürerek evlerimize elektrik sağlar. Doğanın bize sunduğu tertemiz ve tükenmez bir enerjidir rüzgâr. Bazen bir geminin yelkenini doldurur, bazen de sıcak bir günde bizi serinletir."

Sinan, eline küçük bir kağıt uçak alıp rüzgâra doğru fırlattı. Uçak, rüzgârın yardımıyla taklalar atarak uzaklara süzüldü. Rüzgâr estikçe bulutlar gökyüzünde yer değiştiriyor, pamuktan kaleler ve dev balinalar gibi farklı şekillere bürünüyordu. Sinan, rüzgârın aslında doğanın postacısı olduğunu düşündü; çiçeklerin polenlerini uzaklara taşıyor, yağmur yüklü bulutları susuz topraklara ulaştırıyordu.
             
Güneş batarken rüzgâr biraz dindi. Ağaçlar sakinleşti, rüzgâr gülü yavaşladı. Sinan, görünmez dostuna teşekkür etti. Rüzgâr esince dünya sadece hareketlenmiyor, aynı zamanda yaşam için gereken gücü de topluyordu. O gece Sinan, rüzgârın camında fısıldadığı ninnilerle derin bir uykuya daldı."""},
      
        44: {"title": "44. Okuma Parçası: Karışık Tost", "content":"""Cumartesi sabahıydı. Yusuf, mutfaktan gelen tıkırtılarla uyandı. Babası kahvaltıyı hazırlamaya başlamıştı bile. Yusuf, ellerini ve yüzünü yıkayıp mutfağa gittiğinde, babasının ekmekleri hazırladığını gördü. "Baba, bugün kahvaltıyı beraber hazırlayabilir miyiz? Ben de bir 'Karışık Tost' ustası olmak istiyorum!" dedi.

Babası gülümseyerek Yusuf’a küçük bir önlük verdi. "Tabii ki küçük şef! Ama unutma, mutfakta en önemli kural güvenlik ve temizliktir," dedi. Yusuf önce ellerini iyice sabunladı. Sonra babasının gözetiminde malzemeleri hazırlamaya başladı.

Tezgahın üzerinde tam buğday ekmeği, taze kaşar peyniri, ince dilimlenmiş domatesler ve biraz da kekik vardı. Yusuf, ekmeklerin arasına peynirleri özenle yerleştirdi. "Baba, neden buna 'karışık' diyoruz?" diye sordu. Babası, "Çünkü farklı tatlar bir araya gelip yeni ve harika bir lezzet oluşturuyor. Tıpkı bir orkestradaki farklı enstrümanlar gibi," diye cevap verdi.

Yusuf, tost makinesinin ısındığını görünce babasından yardım alarak ekmekleri yerleştirdi. Bir süre sonra mutfağı mis gibi kızarmış ekmek ve eriyen peynir kokusu sardı. Tost makinesinden çıkan "cıs" sesi, Yusuf için dünyanın en güzel müziği gibiydi. Peynirler kenarlardan hafifçe taşmış, ekmekler tam istediği gibi altın sarısı olmuştu.
             
Annesi mutfağa girdiğinde harika kokuyu hemen fark etti. Yusuf, kendi hazırladığı tostu tabağa koyarken gururla, "Afiyet olsun anneciğim, bu tostta sadece peynir yok, biraz da benim sevgim var!" dedi. O sabah yapılan kahvaltı, her zamankinden daha lezzetliydi. Yusuf, bir şeyi kendi emeğiyle hazırlamanın ve sevdikleriyle paylaşmanın ne kadar mutluluk verici olduğunu anlamıştı. Artık o, evlerinin tescilli "Karışık Tost" ustasıydı!"""},
      
        45: {"title": "45. Okuma Parçası: Işık Saklanabilir Mi?", "content":"""Güneşli bir öğleden sonraydı. Can, pencerenin önünde oturmuş, odanın zemininde parlayan güneş ışığını izliyordu. Elini ışığın üzerine koyduğunda avucunun ısındığını fark etti. O sırada aklına ilginç bir soru geldi: "Acaba bu ışığı bir kutuya koysam ve kapağını sıkıca kapatsam, gece olduğunda odamı aydınlatmak için kullanabilir miyim?"

Can hemen boş bir ayakkabı kutusu buldu. Kutuyu en çok güneş alan yere koydu, bir süre bekledi ve kapağını hızla kapattı. Akşam olup hava karardığında büyük bir heyecanla odasına gitti. "Şimdi ışığı serbest bırakma vakti!" diyerek kapağı açtı. Ama o da ne? Kutunun içi kapkaranlıktı. Can biraz üzülmüştü. "Işık neden saklanmıyor?" diye sordu babasına.

Babası gülümseyerek Can’ın yanına oturdu. "Harika bir soru Can! Işık, durmayı sevmeyen, dünyanın en hızlı yolcusudur. Bir saniyede binlerce kilometre yol alır. Kapağı kapattığında ışık kutunun duvarlarına çarpar ve anında enerjiye, yani ısıya dönüşür. Bu yüzden ışığı bir kutuda hapsedemeyiz."

Can merakla sordu: "Peki, güneş panelleri nasıl çalışıyor o zaman?"

"İşte bu harika bir nokta!" dedi babası. "Işığı bir kutuda saklayamayız ama özel teknolojik pillerle onun enerjisini elektriğe dönüştürüp depolayabiliriz. Tıpkı bitkilerin güneş ışığını yapraklarında toplayıp büyümek için kullanması gibi."

Can, ışığın bir kutuda saklanamayacak kadar özgür olduğunu ama dünyadaki tüm canlılara hayat veren gizli bir güç taşıdığını anladı. O gece yatarken el fenerini açtı. Işığın duvardaki dansını izlerken, doğanın ne kadar şaşırtıcı kuralları olduğunu düşünerek hayallere daldı. Işık saklanamıyordu belki ama insanların merakı sayesinde her geçen gün daha farklı şekillerde hayatımızı aydınlatmaya devam ediyordu."""},
      
        46: {"title": "46. Okuma Parçası: Bir Benek Gördüm", "content":"""Cihan ve babası, hafta sonu Toros Dağları’nın eteklerinde uzun bir doğa yürüyüşüne çıkmışlardı. Cihan’ın boynunda bir dürbün, elinde ise gördüğü bitkileri not aldığı küçük bir defter vardı. Babası ona her zaman, "Doğada yürürken sadece ayaklarını değil, gözlerini ve kulaklarını da kullanmalısın," derdi.

Hava serindi ve çam iğnelerinin kokusu her yeri sarmıştı. Bir ara Cihan, sarp kayalıkların arasındaki çalılıkta bir hareketlilik fark etti. Dürbününü hemen gözüne dayadı. Kayaların arasında, tüyleri sarı-kahverengi, üzerinde ise koyu renkli, halka şeklinde benekleri olan uzun bir kuyruk gördü. Kalbi heyecanla güm güm atmaya başladı.

"Baba!" diye fısıldadı Cihan. "Şu kayanın üzerinde bir benek gördüm sanki!"

Babası dikkatle o yöne baktı ama gizemli misafir çoktan ağaçların gölgesinde kaybolmuştu. Babası gülümseyerek Cihan’ın omzuna dokundu. "Eğer gördüğün şey gerçekten oysa Cihan, çok şanslısın. O gördüğün muhtemelen bir Anadolu Parsı’ydı. Onlar ormanlarımızın en gizemli ve en nadir üyeleridir."

Cihan şaşkınlıkla sordu: "Neden bu kadar nadirler baba?"

"Çünkü eskiden yaşam alanları çok daha genişti," dedi babası. "Ama zamanla sayıları azaldı. Şimdi onları korumak için bilim insanları ve doğa severler büyük çaba harcıyor. Onların buralarda olduğunu bilmek, doğanın hala canlı ve sağlıklı olduğunu gösterir."

Cihan, defterine hemen bir benek çizdi. O gün o gizemli benekleri görmek, ona doğanın sadece ağaçlardan ibaret olmadığını öğretmişti. Doğa, korunması gereken binlerce gizli hikaye ve canlıyla doluydu. Cihan artık biliyordu ki; biz doğaya saygı duydukça, o benekli dostlar da dağlarımızda özgürce yaşamaya devam edecekti. Eve dönerken Cihan’ın aklında tek bir düşünce vardı: Ormanın gizli bekçilerini korumak için elinden geleni yapacaktı."""},

        47: {"title": "47. Doğunun İncisi: Van", "content":"""Aylin, sabah uyandığında güneş Van Kalesi'nin üzerinden nazlı nazlı yükseliyordu. Bugün sınıf arkadaşlarına memleketini anlatacağı için içi içine sığmıyordu. Hazırladığı fotoğrafları çantasına koydu ve yola koyuldu.

Sınıfa girdiğinde ilk olarak masmavi bir göl fotoğrafı çıkardı. "Arkadaşlar," dedi neşeyle. "Bu gördüğünüz bir göl değil, biz Vanlılar ona 'Van Denizi' deriz. Çünkü o kadar büyüktür ki baktığınızda sonunu göremezsiniz." Aylin, gölün ortasındaki Akdamar Adası’ndan ve oradaki tarihi kilisenin duvarlarındaki taş işlemelerinden bahsetti. Arkadaşları, adaya gemiyle gidildiğini duyunca çok heyecanlandılar.

Ardından Aylin, herkesin merakla beklediği o meşhur fotoğrafları gösterdi: Bir gözü mavi, diğeri kehribar rengi olan bembeyaz bir Van Kedisi! "Van kedileri sadece renkli gözleriyle değil, suyu sevmeleri ve yüzmeleriyle de ünlüdür," dediğinde sınıfta bir şaşkınlık dalgası yayıldı.

Söz yemeklere gelince Aylin’in sesi daha da heyecanlı çıkmaya başladı. "Van denince akla önce 'Van Kahvaltısı' gelir. Masada yer bulamazsınız; otlu peynir, murtuğa, kavut ve bal... Hepsi birbirinden lezzetlidir." Ayrıca dünyada sadece Van Gölü'nün sodalı suyunda yaşayabilen İnci Kefali’nin, akıntıya karşı zıplayarak yaptığı o mucizevi yolculuğu anlattı.
             
Aylin sunumunu bitirirken, Van'ın binlerce yıllık Urartu tarihine ev sahipliği yaptığını ve her köşesinde ayrı bir hikaye sakladığını söyledi. Arkadaşları Aylin’i alkışlarken, hepsi zihinlerinde Van Denizi'nin kıyısında kahvaltı yapıp Van kedilerini sevdikleri bir hayale dalmışlardı bile. Aylin, memleketinin bu kadar sevilmesinden dolayı gurur duyuyordu."""},
      
        48: {"title": "48. Okuma Parçası: Aynadaki Arkadaşım", "content":"""Umut, o sabah banyoda dişlerini fırçalarken karşısındaki camda kendine bakan o çocuğu izlemeye daldı. O sağ elini kaldırdığında, aynadaki çocuk sol elini kaldırıyordu. Umut gülümsediğinde, o da aynı neşeyle gülümsüyordu. "Acaba," diye düşündü Umut, "aynadaki bu çocuk gerçekten ben miyim, yoksa benim her hareketimi taklit eden gizli bir arkadaşım mı?"

Umut, bu durumu merak edip hemen babasının yanına gitti. "Baba, aynadaki Umut bazen çok garip davranıyor. Ben yaklaştıkça o da yaklaşıyor, ben uzaklaşınca o da küçülüp uzaklaşıyor. Ama her şeyin tersini yapıyor!"

Babası, Umut’un bu merakını çok sevdi. Ona küçük bir el aynası getirerek yansıma kuralını anlatmaya başladı. "Bak Umut, aynalar ışığı geri yansıtan pürüzsüz yüzeylerdir. Üzerine düşen ışık aynaya çarpıp senin gözüne geri döndüğünde, senin bir görüntün oluşur. Buna yansıma diyoruz. Aynadaki görüntü senin tam bir kopyandır ama her şey simetrik olarak tersine döner."

Umut, aynaya bir kağıda yazdığı ismini tuttu. Bir de ne görsün? "UMUT" yazısı aynada sanki başka bir dilde yazılmış gibi ters duruyordu. Babası, "İşte bu yüzden ambulansların önündeki yazılar ters yazılır," dedi. "Böylece öndeki şoför dikiz aynasından baktığında yazıyı düzgün okuyabilir."
             
O gün Umut, aynaların sadece saçımızı taramak için olmadığını öğrendi. Aynalar, ışığın bir oyunuyla bize dünyayı farklı bir açıdan gösteriyordu. Umut tekrar aynanın karşısına geçti, kendine göz kırptı ve fısıldadı: "Merhaba aynadaki arkadaşım! Bugün ikimiz de çok şey öğrendik." Artık yansımasına her baktığında, orada sadece bir görüntü değil, bilimin eğlenceli bir kuralını görüyordu."""},
    
        49: {"title": "49. Okuma Parçası: Memleketim Türkiye", "content":"""Öğretmenimiz o gün sınıfa dev bir Türkiye haritası getirdi. Haritayı tahtaya astığında sınıf bir anda sessizleşti. Her birimiz, sanki üzerinde binbir çiçeğin açtığı kocaman bir bahçeye bakıyor gibiydik. Öğretmenimiz gülümsedi ve "Çocuklar," dedi, "Bugün tek bir şehri değil, hepimizin ortak evi olan memleketimizi konuşacağız."

Ahmet söz aldı: "Öğretmenim, Türkiye her mevsimin aynı anda yaşandığı bir ülke değil mi? Bir yanda Uludağ’da kayak yapılırken, diğer yanda Akdeniz’de pırıl pırıl bir güneş parlıyor." Öğretmenimiz onayladı. Gerçekten de memleketimiz, üç tarafı denizlerle çevrili, dağları bulutlara değen, ovaları bereket saçan eşsiz bir yerdi.

Ayşe, Karadeniz’in yeşil yaylalarını ve çay bahçelerini anlattı. Ardından Adem söz alarak İç Anadolu’nun uçsuz bucaksız bozkırlarını ve peri bacalarını hatırlattı. Doğu Anadolu’nun heybetli kaleleri ve Ege’nin zeytin kokulu kıyıları sanki sınıfımızın içine dolmuştu. Ama Türkiye sadece toprağıyla değil, insanıyla da çok özeldi. Komşusuna bir kap sıcak çorba götüren teyzeler, yolda selamlaşan amcalar ve her köşede neşeyle koşan biz çocuklar, bu memleketin en güzel renkleriydik.

Öğretmenimiz, "Memleket sadece üzerinde yaşadığımız bir toprak parçası değildir," dedi. "Memleket; aynı türkülerle duygulanmak, aynı bayrak altında gururla yürümek ve el ele vererek daha güzel bir gelecek kurmaktır."

O gün hepimiz anladık ki memleketimizi sevmek, onun suyunu, toprağını ve her bir insanını sevmekle başlar. Edirne’den Kars’a, Sinop’tan Hatay’a kadar uzanan bu güzel vatan, bizim en büyük hazinemizdi. Bizler bu hazineyi koruyacak, çok çalışarak onu daha da güzelleştirecek olan küçük fidanlardık. Türkiye, kalbimizin tam ortasında atan kocaman bir sevgiydi."""},
     
        50: {"title": "50. Okuma Parçası: Masallar Diyarı: Kapadokya", "content":"""Melis, o sabah erkenden uyandı. Penceresinden dışarı baktığında gökyüzünün rengarenk balonlarla dolduğunu gördü. Burası Nevşehir’di; yani devlerin ve masalların memleketi! Melis, sınıf arkadaşlarına yaşadığı bu eşsiz şehri tanıtmak için sabırsızlanıyordu.

Okula gittiğinde tahtaya ilginç şekilli kayalar çizdi. "Arkadaşlar," dedi. "Nevşehir denince akla önce Kapadokya gelir. Burası milyonlarca yıl önce volkanların püskürttüğü küllerin ve rüzgarların el ele vererek yaptığı bir sanat eseridir." Melis, kafalarına sanki birer şapka takmış gibi duran o meşhur kayaları gösterdi: "Bunlar Peribacaları! Eskiden insanlar bu kayaların içine evler, pencereler oymuşlar. Hatta güvercinler için küçük saraylar yapmışlar."

Melis daha sonra Avanos ilçesinden bahsetti. Çantasından kırmızı topraktan yapılmış minik bir vazo çıkardı. "Bu toprağın adı kızıl çamur. Kızılırmak’ın kıyısından toplanıyor. Çömlek ustaları bu çamura elleriyle şekil verip onu fırınlıyorlar. Ben de bir gün o döner tezgahın başına geçip kendi vazomu yapmayı hayal ediyorum," dedi.

Sınıfın en çok ilgisini çeken ise yer altı şehirleri oldu. Melis, insanların binlerce yıl önce toprağın altına kat kat şehirler kurduğunu, tünellerle birbirine bağlanan bu gizli dünyalarda yaşadıklarını anlattı. "Sanki yerin altında koca bir labirent var!" diye ekledi.

Güneş batarken Nevşehir’in her köşesi turuncuya boyanırdı. Melis sunumunu bitirirken şöyle dedi: "Bizim memleketimizde her taşın bir hikayesi, her vadinin bir gizemi vardır. Nevşehir, toprağın her katmanında bir hazine saklayan kocaman bir müze gibidir." Arkadaşları Melis’i alkışlarken, hepsi bir gün peribacalarının arasında saklambaç oynamanın hayalini kurmaya başlamıştı."""},
      
        51: {"title": "51. Okuma Parçası: Lili ve İnci", "content":"""İnci, uzun zamandır bir dostun hayalini kuruyordu. Sonunda doğum gününde beklediği sürpriz gerçekleşti: Lili! Lili, bembeyaz tüyleri, neşeli havlamaları ve pamuk şekerine benzeyen kuyruğuyla minik bir köpekti. İnci onu ilk gördüğü anda aralarında kopmayacak bir bağ kurulduğunu hissetti.

Ancak bir köpeğe sahip olmak sadece oyun oynamak demek değildi. Annesi, İnci'ye "Lili artık bizim ailemizin bir üyesi. Onun bakımı ve mutluluğu senin sorumluluğunda," demişti. İnci bu görevi seve seve kabul etti. Her sabah erkenden uyanıyor, Lili’nin mamasını tazeleyip suyunu tazeliyordu. En sevdiği an ise okuldan gelip Lili ile bahçeye çıktığı zamanlardı.

Bir gün parkta yürürken Lili birden durdu ve kulaklarını dikti. Karşıdan gelen başka bir köpeği görmüştü. İnci, Lili'nin biraz çekindiğini fark etti. Hemen yanına çömeldi ve başını okşayarak, "Korkma Lili, ben buradayım," diye fısıldadı. Lili, İnci'nin sesindeki güveni hissedince sakinleşti. O an İnci, dostluğun sadece beraber koşmak değil, birbirine zor anlarda destek olmak olduğunu da anladı.

Lili büyüdükçe İnci de onunla beraber büyüyordu. Lili’ye "otur", "patini ver" gibi komutları sabırla öğretti. Sabretmeyi, karşılık beklemeden sevmeyi ve bir canlının sorumluluğunu almanın ne kadar gurur verici olduğunu Lili sayesinde keşfetti. Akşamları İnci ödevlerini yaparken Lili onun ayaklarının dibine kıvrılıyor, sanki ona moral veriyordu.

Artık İnci için Lili sadece bir evcil hayvan değil, sırlarını paylaştığı en yakın arkadaşıydı. Bembeyaz tüylerin arasındaki o sevgi dolu gözler, İnci’ye her gün dünyanın en güzel dilinin "sevgi" olduğunu hatırlatıyordu."""},
       
        52: {"title": "52. Okuma Parçası: Zeka Oyunlarının Kilidi: Bilmeceler", "content":"""Zeki ve Asuman, yağmurlu bir öğleden sonra dedelerinin yanına, şömine başına sokuldular. Televizyon kapalıydı ama odanın içi neşeyle doluydu. Dedesi gülümseyerek, "Hadi bakalım çocuklar," dedi. "Zihinlerimizi tazelemeye ne dersiniz? Size birkaç tane 'akıl kilidi' soracağım. Bakalım kim anahtarı önce bulacak?"

Asuman merakla atıldı: "Akıl kilidi de nedir dede?"

Dedesi, "Bilmecedir elbet!" diyerek ilkini sordu: "Şehirleri var, evleri yok. Dağları var, ağaçları yok. Suları var, balıkları yok. Nedir bu?"

Zeki ve Asuman bir süre düşündüler. Zeki, "Buldum! Bu bir harita!" diye bağırdı. Dedesi aferin diyerek ikinciyi sordu: "Benim bir arkadaşım var, ben nereye gidersem o da oraya gider. Ben durursam o da durur. Güneş gidince o da kaybolur." Asuman hemen cevabı yapıştırdı: "Gölge!"

Bilmeceler sadece birer soru değil, kelimelerin saklambaç oynaması gibiydi. Nesnelerin özelliklerini doğrudan söylemek yerine, onları farklı kılıklara sokarak anlatırlardı. Dedesi onlara bilmecelerin çok eski bir gelenek olduğunu, insanların eskiden kış gecelerini bu şekilde birbirlerine sorular sorarak geçirdiklerini anlattı. Bilmeceler; dikkatli bakmayı, benzerlikleri fark etmeyi ve hızlı düşünmeyi öğretiyordu.

Akşam boyunca "Çarşıdan aldım bir tane, eve geldim bin tane" (Nar) ve "Kanadı var uçamaz, karada da kaçamaz" (Balık) gibi pek çok bilmece havada uçuştu. Zeki ve Asuman o gün anladılar ki, kelimelerle oynamak en az bilgisayar oyunları kadar eğlenceliydi. Bilmeceler, her seferinde yeni bir kapı açan sihirli anahtarlar gibiydi ve en güzel yanı da sonunda kocaman bir gülümseme bırakmasıydı."""},

        53: {"title": "53. Okuma Parçası: Çık Ortaya", "content":"""Güneşli bir okul sonrasıydı. Mahallenin çocukları büyük çınar ağacının altında toplandı. Herkesin gözünde aynı heyecan vardı: "Saklambaç oynayalım mı?" diye bağırdı Arda. Hep bir ağızdan "Evet!" sesleri yükseldi. Hemen bir ebe seçmek için tekerleme söylenmeye başlandı: "Komşu komşu hu hu, oğlun geldi mi? Geldi..." Tekerleme bittiğinde ebe Fatma olmuştu.

Fatma, gözlerini çınar ağacının gövdesine yasladı ve yüksek sesle saymaya başladı: "On, yirmi, otuz... Sağım solum sobe, saklanmayan ebe!" O sayarken diğerleri nefes nefese kendilerine en güvenli yerleri bulmaya çalıştı. Ahmet, büyük bir çöp kutusunun arkasına büzüldü; Zeynep ise leylak çalılarının arasına adeta gizlendi.

Fatma saymayı bitirip gözlerini açtığında mahalle sessizliğe bürünmüştü. "Çık ortaya, seni görüyorum!" diye şaka yaparak etrafı kontrol etmeye başladı. Saklambaç sadece bir oyun değildi; aynı zamanda strateji kurmak ve sessiz kalabilmek demekti. Fatma, Ahmet’in ayakkabı ucunu fark edince hızla ağaca doğru koştu: "Sobe Ahmet!"

Oyun ilerledikçe kahkahalar mahalleyi sardı. En sonunda herkes sobelenmiş ya da kurtulmuştu. Oyunun en güzel kuralı ise dürüstlüktü. Kimse sırasını bozmadı, kimse "gördüm" demeden sobelemedi. Yorulup ağacın gölgesine oturduklarında, Arda "Geleneksel oyunlar ne kadar eğlenceli, değil mi?" dedi. Televizyonun veya tabletin karşısında tek başına vakit geçirmektense, arkadaşlarıyla "Çık ortaya!" diye bağırmak paha biçilemezdi.

Akşam ezanı okunurken çocuklar evlerine dağıldı. Arkalarında sadece tatlı bir yorgunluk ve bir sonraki oyunun planlarını bıraktılar. Çünkü biliyorlardı ki oyun, çocukları birbirine bağlayan en güçlü köprüydü."""},

        54: {"title": "54. Okuma Parçası: Beyaz", "content":"""Faruk o sabah uyandığında odasının her zamankinden daha aydınlık olduğunu fark etti. Perdesini araladığında dışarıda muhteşem bir manzara vardı: Gece boyunca yağan kar, bütün şehri bembeyaz bir masal diyarına çevirmişti. Ağaçlar beyaz elbiselerini giymiş, sokaklar tertemiz bir sayfa gibi uzanıyordu.

Faruk, "Beyaz ne kadar da güçlü bir renk!" diye düşündü. Sadece dışarıdaki kar değil, hayatındaki pek çok güzel şey beyazdı. Annesinin sabah masaya bıraktığı bir bardak süt, bembeyaz bir kağıt, gökyüzünde süzülen pamuk gibi bulutlar... Okulda öğretmeni beyazın tüm renklerin birleşimi olduğunu anlatmıştı. "Beyaz, içinde bütün renkleri saklar," demişti öğretmeni. "Bu yüzden o hem temizliğin hem de yeni başlangıçların rengidir."

[Image representing the visible light spectrum coming from white light passing through a prism]

Faruk dışarı çıkıp karın üzerine ilk adımını attığında, bembeyaz örtünün üzerinde kendi ayak izlerini gördü. Sanki beyaz bir kağıda resim çiziyor gibiydi. O sırada beyaz bir güvercinin çatıdan havalandığını gördü. Babası, beyaz güvercinlerin dünyada "barış" anlamına geldiğini söylemişti. Faruk, beyazın sadece bir renk değil, aynı zamanda dostluk ve huzur demek olduğunu o an bir kez daha anladı.
Akşam eve dönüp sıcak çikolatasını içerken, beyazın hayatımızdaki yerini daha iyi kavradı. Doktorların önlükleri, dişlerimizin sağlığı ve gökyüzündeki yıldızların parıltısı hep o saflığı taşıyordu. Beyaz, dünyayı daha aydınlık ve daha umut dolu gösteriyordu. Faruk, bembeyaz kağıdını önüne aldı ve üzerine renkli kalemleriyle hayallerini çizmeye başladı. Biliyordu ki, en güzel resimler her zaman o temiz ve beyaz sayfada başlardı."""},
        
        55: {"title": "55. Okuma Parçası: Tarladaki Dev Güç: Biçerdöver", "content":"""Mahmut, yaz tatilini geçirmek için dedesinin köyüne gitmişti. Bir sabah tarladan gelen gürültülü ama düzenli bir sesle uyandı. Pencereden baktığında, altın sarısı buğday tarlasının içinde dev bir makinenin ağır ağır ilerlediğini gördü. Bu makine kocaman dişleri olan, kırmızı renkli bir canavara benziyordu!

Hemen dedesinin yanına koştu. "Dede, o dev makine tarlada ne yapıyor? Sanki buğdayları yiyor!" dedi merakla.

Dedesi gülerek Mahmut’un elinden tuttu. "O bizim en büyük yardımcımız Mahmut, adı biçerdöver. İsmi biraz ilginçtir ama yaptığı iş çok kıymetlidir. Bak bakalım, neden hem 'biçer' hem de 'döver' diyorlar?"

Mahmut dikkatle izlemeye başladı. Makinenin önündeki dönen dişliler buğdayları kesiyor, yani biçiyordu. Dedesi anlatmaya devam etti: "Makine buğdayları biçtikten sonra onları içine alır. Orada sapları ve çöpleri buğday tanelerinden ayırır. İşte bu ayırma işlemine eskiden 'dövme' denirdi. Yani biçerdöver; buğdayı tarladan keser, tanesini kabuğundan ayırır ve tertemiz bir şekilde deposunda biriktirir."

Mahmut hayretler içindeydi. Eskiden insanların haftalarca uğraşarak yaptığı işi, bu dev makine birkaç saatte bitiriyordu. Biçerdöverin arkasından ise tarlaya sarı samanlar dökülüyordu. Dedesi, "O samanlar da kışın hayvanlarımıza yiyecek ve yatak olacak," dedi.
             
O gün Mahmut, sofrasına gelen ekmeğin sadece fırından çıkmadığını anladı. O ekmeğin içinde güneşin sıcaklığı, toprağın bereketi ve biçerdöverin emeği vardı. Akşam yemeğinde ekmeğini bölerken, tarladaki o dev dostunu ve çiftçilerin zorlu ama güzel yolculuğunu düşünerek teşekkür etti."""},

        56: {"title": "56. Okuma Parçası: Çiçekli Pasta", "content":"""Bahar mevsiminin en renkli günlerinden biriydi. Melek, bahçelerindeki papatyaların ve mor menekşelerin neşeyle güneşe gülümsediğini gördü. Bugün annesinin doğum günüydü ve Melek ona unutamayacağı bir sürpriz yapmak istiyordu. Mutfağa gidip büyük ablasına "Abla, annem için dünyanın en güzel pastasını yapalım mı?" diye sordu.

Ablası bu fikre bayıldı. Hemen önlüklerini taktılar. Mutfakta hummalı bir çalışma başladı. Yumurtalar kırıldı, un elendi ve fırından mis gibi vanilya kokuları yayılmaya başladı. Ancak Melek, pastanın sadece tadının değil, görüntüsünün de çok özel olmasını istiyordu. "Abla," dedi, "Pastamızın üzerine şekerden süsler koymak yerine, bahçemizdeki gerçek çiçekleri kullansak nasıl olur?"

Ablası bunun harika bir fikir olduğunu ama sadece "yenilebilir" çiçekleri seçmeleri gerektiğini söyledi. Melek, bahçeye koşup özenle birkaç tane hercai menekşe ve mis kokulu gül yaprağı topladı. Çiçekleri incitmeden yıkadılar ve kuruladılar. Pastanın üzerine bembeyaz bir krema sürdükten sonra, Melek topladığı renkli yaprakları bir ressam titizliğiyle pastanın üzerine dizmeye başladı.

Sonunda pasta bittiğinde karşılarında bir yiyecek değil, adeta minik bir bahçe duruyordu. Akşam annesi eve gelip masanın ortasındaki "Çiçekli Pasta"yı görünce gözlerine inanamadı. "Hayatımda gördüğüm en zarif hediye bu!" diyerek çocuklarına sarıldı.

O akşam hep birlikte pastalarını yerken Melek şunu düşündü: Doğanın sunduğu güzellikler, en süslü oyuncaklardan veya şekerlemelerden çok daha değerliydi. Sevgiyle yapılan bir işe doğanın renkleri de eklenince, ortaya çıkan sonuç herkesin kalbini ısıtıyordu. Melek o gün, yaratıcılığın ve emeğin en güzel süs olduğunu öğrenmişti."""},

        57: {"title": "57. Taşların Dile Geldiği Şehir", "content":"""Ali, o sabah güneşin ilk ışıklarıyla uyandı. Penceresinden dışarı baktığında, şehri kaplayan sarımtırak taş evlerin sanki birer altın gibi parladığını gördü. Mardin, bir tepenin yamacına kurulmuş, evlerin birbirinin manzarasını kapatmadığı, adeta basamaklı bir merdivene benzeyen masalsı bir şehirdi.

Ali, bugün okulda "Benim Güzel Şehrim" konulu bir sunum yapacaktı. Çantasına babasının gümüşten yaptığı küçük bir telkari kolye ve bir avuç mavi badem şekeri koydu. Okula giderken daracık, labirent gibi sokaklardan geçti. Bu sokaklara "abbara" deniyordu. Bazıları evlerin altından tünel gibi geçiyor, Ali’ye her seferinde gizli bir geçitteymiş hissi veriyordu.

Sınıfa girdiğinde sunumuna başladı: "Arkadaşlar," dedi. "Mardin demek, taşın şiir gibi işlendiği yer demektir. Bizim evlerimiz taştan yapılmıştır; bu yüzden yazın serin, kışın ise sıcacık olur. Ama Mardin sadece taşlardan ibaret değildir. Bizim şehrimizde farklı dillerden, farklı inanışlardan insanlar tıpkı bir ebru sanatı gibi bir arada, huzurla yaşarlar."

Ali, elindeki gümüş telkariyi gösterdi. "Bu gördüğünüz sanat, gümüş tellerin incecik işlenmesiyle yapılıyor. Sabır ve dikkat istiyor, tıpkı Mardin’in tarihi gibi..." Sonra mavi badem şekerlerini arkadaşlarına ikram etti. Arkadaşları hem şekerlerin rengine hem de Ali'nin anlattığı masalsı şehre hayran kaldılar.

Sunumunun sonunda Ali, akşamları şehrin ışıkları yanınca Mardin’in uzaktan bir "gece gerdanlığına" benzediğini anlattı. Mardin’e yukarıdan bakınca uçsuz bucaksız Mezopotamya ovası bir deniz gibi ayaklarınızın altına serilirdi. Arkadaşları o gün Ali’yi dinlerken sadece bir şehri öğrenmediler, aynı zamanda tarihe ve farklılıklara saygı duymanın ne kadar güzel olduğunu da hissettiler."""},
      
        58: {"title": "58. Okuma Parçası: Denizli", "content":"""Güneş, Ege’nin iç kesimlerini ısıtırken, Kaan elindeki fotoğrafları heyecanla sırasına dizdi. Bugün sınıfta arkadaşlarına, dedesinin memleketi olan Denizli’yi anlatacaktı. Fotoğrafların en üstünde, bembeyaz bir pamuk yığınını andıran devasa basamaklar duruyordu.

"Arkadaşlar," diyerek söze başladı Kaan. "Burası Pamukkale. Ama buradaki beyazlık kar değil, şifalı suların binlerce yıl boyunca kayaların üzerinde bıraktığı özel bir maddedir. İnsanlar bu bembeyaz havuzların içine girip yürüyebiliyorlar. Pamukkale’nin hemen yanı başında ise Hierapolis adında, taşların diliyle konuşan çok eski bir antik kent var."

Sınıftaki arkadaşları şaşkınlıkla fotoğraflara bakarken Kaan ikinci fotoğrafı gösterdi. Bu, ibiği kıpkırmızı, tüyleri ise gökkuşağı gibi parlayan yakışıklı bir horozdu. "İşte bu meşhur Denizli Horozu!" dedi Kaan gururla. "Onun en önemli özelliği, o kadar uzun ve güzel öter ki, nefesi yetmeyince bazen olduğu yere bayılıverir. Bu yüzden şehrin tam ortasında onun kocaman bir heykeli bulunur."

Kaan son olarak yanına getirdiği yumuşacık bir havluyu masaya koydu. "Denizli sadece bir turizm şehri değil, aynı zamanda Türkiye'nin dokuma merkezidir. Babamın anlattığına göre, Buldan ilçesinde binlerce yıldır kumaşlar dokunur. Bugün dünyanın pek çok yerindeki insanlar, Denizli’de üretilen bu kaliteli bornozları ve havluları kullanıyor."

Sunumun sonunda Kaan, Denizli'nin hem bembeyaz travertenleriyle bir masal diyarı hem de çalışkan insanlarıyla bir sanayi şehri olduğunu söyledi. Arkadaşları o gün, bir şehrin nasıl hem tarih hem de üretimle bu kadar zenginleşebileceğini Kaan sayesinde öğrendiler. Kaan, kürsüden inerken memleketinin bu eşsiz güzelliklerini herkesle paylaşmış olmanın mutluluğunu yaşıyordu."""},
      
        59: {"title": "59. Okuma Parçası: Gökyüzünün Ötesinde", "content":"""Umut, o akşam bahçedeki şezlonga uzanmış, gökyüzündeki parıl parıl yanan yıldızları saymaya çalışıyordu. Yanına gelen ablası Defne, elindeki tabletten bir görüntü gösterdi. Görüntüde, devasa bir roketin dumanlar içinde gökyüzüne doğru yükseldiği anlar vardı.

"Bak Umut," dedi Defne. "Bunlar günümüzün cesur kaşifleri, yani astronotlar. Bilinmeze doğru, yıldızların arasına yolculuk yapıyorlar."

Umut merakla sordu: "Peki abla, orada nasıl yaşıyorlar? Yerçekimi yoksa yemeklerini nasıl yiyorlar, nasıl uyuyorlar?"

Defne anlatmaya başladı: "Uzay istasyonunda yaşamak, dünyadakinden çok farklıdır. Orada her şey havada süzülür. Bu yüzden astronotlar uyurken kendilerini duvara bağlı tulumlara yerleştirirler ki gece boyu bir yerlere çarpmasınlar. Yemekleri ise genellikle özel paketlerdedir. Bir damla su bile havada minik bir top gibi süzüldüğü için, her şeyi çok dikkatli yapmaları gerekir."

Umut, gökyüzüne bakıp o devasa roketin içinde olduğunu hayal etti. Dünyamız, uzaydan bakıldığında masmavi, parlak bir bilye gibi görünüyordu. Astronotlar orada sadece gezmek için değil; bitkilerin uzayda nasıl büyüdüğünü anlamak, yeni ilaçlar geliştirmek ve evrenin sırlarını çözmek için deneyler yapıyorlardı.

"Ben de bir gün o özel kıyafeti giyip uzay yolcusu olmak istiyorum," dedi Umut kararlılıkla. "Belki de başka gezegenlerde su olup olmadığını ben bulurum!"

Defne kardeşinin saçlarını okşadı. "Bunun için çok çalışman, matematiği ve fen bilimlerini sevmen gerekiyor Umut. Ama unutma, her büyük yolculuk önce bir hayalle başlar."

O gece Umut, rüyasında parlayan yıldızların arasından süzülerek geçtiğini ve Ay'ın yüzeyinde ilk adımlarını attığını gördü. Gökyüzü artık onun için sadece karanlık bir boşluk değil, keşfedilmeyi bekleyen devasa bir oyun alanıydı."""},
      
        60: {"title": "60. Okuma Parçası: Cesur Kaşifler: Astronotlar", "content":"""Alper ve Esin, o gün okulun kütüphanesinde devasa bir uzay ansiklopedisi buldular. Sayfaları çevirdikçe karşılarına çıkan parıltılı dünyalar, onları uzak diyarlara götürdü. Kitabın en heyecan verici bölümü ise uzay yolcularını, yani astronotları anlatan kısımdı.

"Esin, baksana!" dedi Alper heyecanla. "Astronotlar uzaya gitmeden önce yıllarca eğitim alıyorlarmış. Su altında dev havuzlarda saatlerce antrenman yapıyorlar ki uzaydaki ağırlıksız ortama alışabilsinler."

Esin, bir astronotun uzay başlığı içindeki fotoğrafına bakarak ekledi: "Sadece bu da değil! Uzayda yemek yemek bile bir macera. Yerçekimi olmadığı için çorbalarını kaşıkla içemiyorlar, çünkü her şey havada uçuşuyor! Yemekleri özel vakumlu paketlerden, pipetle veya küçük lokmalar halinde tüketmek zorundalar."

İki arkadaş, uzay istasyonunda yaşamanın nasıl bir his olduğunu hayal etmeye başladılar. Astronotlar orada sadece vakit geçirmiyor; bitkilerin susuz ortamda nasıl yetiştiğini gözlemliyor, gökyüzündeki dev teleskopları tamir ediyor ve Dünyamızın daha iyi anlaşılması için bilimsel deneyler yapıyorlardı. Onlar, insanlığın bilinmeyene açılan gözleri gibiydiler.

Alper, "Bir gün ben de o roketin içinde olmak istiyorum," dedi. "Dünyamıza dışarıdan bakıp ne kadar değerli olduğunu kendi gözlerimle görmeyi hayal ediyorum."

Esin de ona katıldı: "O zaman şimdiden hazırlanmalıyız Alper. Astronot olmak için sadece cesur olmak yetmez; matematiği sevmek, sağlıklı beslenmek ve doğayı korumak da gerekir. Çünkü uzay yolculuğu, büyük bir disiplin ve ekip çalışmasıdır."

Zil çalıp sınıfa dönerken, ikisinin de aklında aynı görüntü vardı: Masmavi bir gökyüzü ve onun ötesinde keşfedilmeyi bekleyen binlerce yıldız. Belki de bir gün, bu küçük okulun sıralarından çıkan bir çocuk, Ay’ın tozlu yollarında kendi ayak izlerini bırakacaktı."""},
      
        61: {"title": "61. Okuma Parçası: Kardan Adamın Gülümsemesi", "content":"""O gece gökyüzünden sessizce milyonlarca beyaz tüy döküldü. Sabah olduğunda bahçe, parıl parıl parlayan beyaz bir örtüyle kaplanmıştı. Deniz ve Itıl, heyecanla dışarı fırladılar. Elleriyle karı yuvarlayıp üst üste koydular ve kısa sürede kocaman, havuç burunlu, kömür gözlü bir kardan adam yaptılar.

Akşam olup hava iyice soğuduğunda, Deniz pencereden kardan adama bakarken birden duraksadı. "Itıl, sence kardan adamımız orada tek başına hiç üşüyor mudur?" diye sordu. Hava o kadar ayazdı ki, camlar bile buğulanmıştı. "Biz içeride battaniyelerimizin altındayız ama o dışarıda rüzgara karşı duruyor."

Itıl biraz düşündü. "Hadi ona gidip bir atkı ve bere takalım!" dedi. İki kardeş, eski bir atkıyı kardan adamın boynuna doladılar ve başına yırtık bir şapka taktılar. Ama Deniz’in içindeki merak bitmemişti. Babasına gidip sordu: "Babacığım, kardan adama atkı taktık ama o hala buz gibi. Acaba canı yanıyor mudur?"

Babası çocukları yanına çağırdı ve gülümsedi. "Çocuklar, kardan adamlar bizim gibi değildir," dedi. "Onların en büyük düşmanı soğuk değil, sıcaktır. Onlar kışın buz gibi rüzgarını severler, çünkü o soğuk hava onları ayakta tutar. Eğer kardan adama sıcak bir mont giydirip eve alsaydınız, üşümekten kurtulmaz, tam tersine eriyip yok olurdu. Onun için atkı takmanız çok güzel bir incelik ama merak etmeyin, o şu an dünyanın en mutlu ve en 'serin' arkadaşı!"

Deniz ve Itıl bu duruma çok şaşırdılar. Kardan adam üşümüyordu; aksine kışın soğuğu onun can suyu gibiydi. O gece yataklarına yattıklarında, dışarıdaki dostlarının atkısıyla rüzgara karşı neşeyle gülümsediğini biliyorlardı. Doğa ne kadar ilginçti; birimiz için dondurucu olan soğuk, bir diğeri için en güzel yaşam alanı olabiliyordu."""},
       
        62: {"title": "62. Okuma Parçası: Hayal Kurmak", "content":"""Güneşli bir öğleden sonraydı. Eren, odasındaki pencerenin kenarına oturmuş, gökyüzündeki pamuk bulutları izliyordu. Bulutlardan biri kocaman bir balinaya, diğeri ise çatısı dondurmadan yapılmış bir şatoya benziyordu. Eren’in elinde sadece boş bir kağıt ve bir kurşun kalem vardı ama zihninin içi binlerce renkle doluydu.

Annesi içeri girdiğinde Eren’in dalgın dalgın dışarı baktığını gördü. "Neler düşünüyorsun küçük ressam?" diye sordu. Eren gülümseyerek, "Hayal kuruyorum anneciğim," dedi. "Bulutların üzerinde koşan bir robot tasarlıyorum. Ayakları yaylı olduğu için zıpladıkça yıldızlara değiyor!"

Annesi Eren’in yanına oturdu ve hayal kurmanın ne kadar değerli olduğunu anlatmaya başladı. "Biliyor musun Eren, bugün dünyada gördüğümüz bütün harika icatlar önce birinin hayaliyle başladı. Birileri gökyüzünde kuşlar gibi uçmayı hayal etmeseydi uçaklar yapılamazdı. Ya da birileri karanlık geceleri aydınlatmayı düşlemeseydi ampul hiç bulunamazdı."

Hayal kurmak, sadece eğlenceli bir oyun değil, aynı zamanda beynimizin bir antrenmanı gibiydi. Hayal kurarken imkansız diye bir şey yoktu. Okyanusun en derin yerine inebilir, görünmez bir pelerin giyebilir ya da hayvanlarla konuşabilirdik. Bu hayaller, büyüdüğümüzde bize yeni kapılar açan, sorunlara farklı çözümler bulmamızı sağlayan birer pusulaydı.

Eren o günden sonra her gün "hayal kurma saati" yapmaya karar verdi. Çünkü biliyordu ki; bir şeyi önce zihninde canlandırabilirse, onu gerçekleştirmek için gerekli gücü de kendinde bulabilirdi. Elindeki kalemi kağıda dokundurdu ve az önce hayal ettiği o yaylı robotu çizmeye başladı. Artık o sadece bir kağıt parçası değil, Eren'in gelecekteki büyük keşiflerinin ilk adımıydı."""},
      
        63: {"title": "63. Okuma Parçası: Ağaç Doktorları", "content":"""Sarp ve Maya, hafta sonu babalarıyla birlikte ormanda uzun bir yürüyüşe çıkmışlardı. Kuş seslerini dinlerken, ileride turuncu yelek giymiş, ellerinde garip aletler olan bir grup insan gördüler. Bu kişiler, bazı ağaçların gövdelerini inceliyor, notlar alıyor ve sanki ağaçlarla konuşuyorlardı.

Sarp merakla babasına sordu: "Baba, bu insanlar ağaçlara ne yapıyorlar? Yoksa ağaçları mı kesecekler?"

Babası gülümseyerek çocukları o grubun yanına götürdü. "Hayır Sarp, tam tersine! Onlar ormanın sağlığını koruyan ağaç doktorları, yani orman mühendisleri ve teknisyenleri," dedi.

Doktorlardan biri, elindeki ince uzun çubuğu göstererek çocuklara yaklaştı. "Merhaba çocuklar! Biz tıpkı sizin doktorlarınız gibi ağaçların hasta olup olmadığını kontrol ediyoruz. Onların kabuklarını muayene ediyor, yapraklarındaki renk değişimlerine bakıyoruz. Eğer bir ağaç böcekler yüzünden hastalanmışsa veya yeterince su alamıyorsa, ona nasıl yardım edebileceğimizi planlıyoruz."

Maya şaşkınlıkla sordu: "Peki, ağaçlar gerçekten iyileşebilir mi?"

"Elbette," dedi ağaç doktoru. "Bazen ağacın hasta olan dalını budarız, bazen de toprağına ihtiyacı olan mineralleri ekleriz. Sağlıklı bir ağaç, binlerce canlıya yuva olur ve bize tertemiz nefes verir. Bizim görevimiz, bu koca ormanın nefesinin kesilmemesini sağlamak."

O gün Sarp ve Maya, doktorluğun sadece insanlar için olmadığını öğrendiler. Ağaçlar da tıpkı bizler gibi ilgiye, sevgiye ve bazen de tedaviye ihtiyaç duyuyorlardı. Eve dönerken ormandaki her bir ağaca daha dikkatli baktılar. Artık biliyorlardı ki, bu devasa yeşil devlerin de görünmez kahramanları, yani doktorları vardı."""},
       
        64: {"title": "64. Okuma Parçası: Bir Elma İki Arkadaş", "content":"""Caner, okula henüz yeni başlamıştı ve teneffüslerde ne yapacağını bilemiyordu. Okul bahçesi çok kalabalık, çocuklar ise çok hareketliydi. Caner, bahçedeki yaşlı çınar ağacının altına oturdu ve çantasından annesinin koyduğu kıpkırmızı, sulu bir elmayı çıkardı. Tam elmasından bir ısırık alacaktı ki, yanında birinin durduğunu fark etti.

Bu, sınıftan arkadaşı Bora idi. Bora’nın üzgün bir hali vardı. Caner, "Neyin var Bora?" diye sordu. Bora, beslenme çantasını evde unuttuğunu ve karnının çok acıktığını söyledi. Caner bir elmasına baktı, bir de arkadaşına. Paylaşmanın, tek başına yemekten çok daha güzel olduğunu biliyordu.

"Üzülme," dedi Caner gülümseyerek. "Bu elma ikimiz için de yeterli!" Elmayı tam ortadan ikiye bölüp yarısını Bora’ya uzattı. Bora’nın gözleri parladı, "Çok teşekkür ederim Caner, sen çok nazik bir arkadaşsın," dedi. Birlikte elmalarını yerken bir yandan da sohbet etmeye başladılar. Caner en sevdiği oyunları anlattı, Bora ise evdeki kedisinden bahsetti.

O gün o kırmızı elma, sadece karınlarını doyurmamış, aralarında sıcacık bir köprü kurmuştu. Teneffüs zili çaldığında artık ikisi de yalnız değildi. Caner, paylaşmanın sihirli bir gücü olduğunu anlamıştı; bir elmayı ikiye böldüğünde elma küçülmüştü ama kalbindeki mutluluk iki katına çıkmıştı.

Ertesi gün bu sefer Bora, yanında getirdiği iki tane kurabiyeden birini Caner'e uzattı. Artık okul bahçesindeki o yaşlı çınar ağacı, sadece bir gölge yeri değil, harika bir arkadaşlığın başladığı özel bir duraktı. Çocuklar o günden sonra sadece yiyeceklerini değil, oyunlarını ve hayallerini de paylaşmaya devam ettiler."""},
       
        65: {"title": "65. Okuma Parçası: Pistteki Rüzgar", "content":"""Aras, okulun spor bayramı için günlerdir hazırlık yapıyordu. Onun en büyük hayali, 100 metre koşusunda birinci gelip "okulun en hızlı atleti" unvanını almaktı. Her sabah erkenden uyanıyor, parkta antrenman yapıyor ve sağlıklı besleniyordu. Çünkü Aras biliyordu ki sporcu olmak sadece hızlı koşmak değil, aynı zamanda vücuduna iyi bakmak demekti.

Yarış günü gelip çattığında, tribünler heyecanlı veliler ve öğrencilerle doluydu. Aras başlangıç çizgisine geldiğinde kalbi küt küt atıyordu. Yan kulvarda en yakın arkadaşı Kerem vardı. Hakem, "Yerlerinize, hazır, başla!" dediğinde Aras sanki bir ok gibi yayından fırladı. Rüzgarın yüzüne çarpışını, ayaklarının altındaki pistin hızla akıp gidişini hissetmek harikaydı.

Yarışın ortasında, tam Aras öne geçmek üzereyken, yan kulvardaki Kerem’in ayağı takıldı ve dengesi sarsıldı. Aras o an bir seçim yapmak zorundaydı: Ya sadece yarışı kazanmaya odaklanacak ya da arkadaşına yardım edecekti. Aras hızını biraz yavaşlatıp Kerem’e "Haydi Kerem, başarabilirsin, bırakma!" diye bağırdı. Bu destek Kerem’e güç verdi, dengesini topladı ve ikisi de bitiş çizgisine neredeyse aynı anda ulaştı.

Aras yarışı milimetre farkıyla birinci bitirdi. Ancak madalyasını alırken sadece hızlı olduğu için değil, sergilediği bu güzel davranış için de alkışlandı. Öğretmeni ona, "Gerçek bir atlet, sadece bacaklarıyla değil, kalbiyle de koşar Aras. Sen bugün hem en hızlı olduğunu hem de gerçek bir centilmen olduğunu kanıtladın," dedi.

Aras o gün eve dönerken altın madalyasından daha değerli bir şey kazandığını anladı: Dostluk ve dürüst oyun. En hızlı olmak güzeldi ama en iyi karakterli sporcu olmak çok daha gurur vericiydi. Artık bir sonraki yarışı için daha büyük bir heyecanla antrenmanlarına devam edecekti."""},
       
        66: {"title": "66. Okuma Parçası: Ayşe'nin Sihirli Ayakkabıları", "content":"""Ayşe, o sabah dolabını açtığında en sevdiği kırmızı ayakkabılarına baktı. Bu ayakkabılar onun için sadece bir eşya değildi; onlarla parkta en hızlı o koşmuş, bahçedeki kedilerle en neşeli oyunları o oynamıştı. Ancak o gün bir gariplik vardı. Ayşe, ayakkabılarını giymeye çalıştığında parmaklarının ucunun sıkıştığını fark etti.

"Anne!" diye seslendi Ayşe. "Sanırım ayakkabılarım gece uyurken küçülmüş!"

Annesi gülümseyerek Ayşe’nin yanına geldi. Ayşe’nin boyunu kapının kenarındaki boy cetveliyle ölçtü. "Hayır Ayşe," dedi annesi. "Ayakkabıların küçülmedi, sen biraz daha büyüdün. Bak, geçen aya göre boyun tam iki santimetre uzamış."

Ayşe bir yandan büyümesine seviniyor, bir yandan da kırmızı ayakkabılarından ayrılacağı için üzülüyordu. Onları eline aldı ve üzerindeki küçük çamur lekelerine baktı. Her leke, bir maceranın hatırasıydı. Annesi, "Eşyalarımızla vedalaşmak bazen zordur ama onlar görevlerini tamamladığında yeni bir yolculuğa çıkabilirler," dedi.

Birlikte kırmızı ayakkabıları güzelce temizlediler ve parlatıp kutusuna koydular. Bu ayakkabılar artık komşularının minik kızı Lale’ye gidecekti. Ayşe, ayakkabıların içine küçük bir not bıraktı: "Bu ayakkabılar çok hızlı koşar ve sahibini çok mutlu eder. İyi yolculuklar!"

Ertesi gün Ayşe’ye yeni ve bir numara büyük ayakkabılar alındı. Bu yeni ayakkabılar gıcır gıcırdı ve çok havalı duruyordu. Ayşe, yeni ayakkabılarıyla ilk adımını atarken şunu düşündü: Büyümek sadece boyun uzaması değil, aynı zamanda sahip olduklarını başkalarıyla paylaşabilmek ve yeni maceralara hazır olmaktı. Eski ayakkabıları Lale ile yeni oyunlar kurarken, Ayşe de yeni ayakkabılarıyla daha yüksek yerlere uzanacaktı."""},
       
        67: {"title": "67. Okuma Parçası: Birlikte Güçlüyüz", "content":"""Okulun arka bahçesindeki basketbol sahası, o gün büyük bir heyecana ev sahipliği yapıyordu. Dördüncü sınıflar arasında düzenlenen "Dostluk Turnuvası" final maçı başlamak üzereydi. Mete’nin takımı sahaya çıktığında herkes biraz gergindi. Karşı takım çok güçlü görünüyordu ve Mete, "Acaba kazanabilir miyiz?" diye düşünmeden edemiyordu.

Öğretmenleri Hakan Bey, çocukları yanına çağırdı ve hepsinin gözlerinin içine bakarak şunları söyledi: "Çocuklar, şampiyon olmak sadece en çok sayıyı atmak değildir. Gerçek şampiyonluk, paslaştığınızda, arkadaşınız düştüğünde elinden tuttuğunuzda ve birbirinize güvendiğinizde başlar. Unutmayın, sahada beş kişi değil, tek bir yürek olmalısınız."

Maç başladığında işler başta zor gitti. Selin çok hızlı koşuyor ama potaya topu ulaştıramıyordu. Can boyu uzun olduğu için ribaundları topluyor ama pas verecek kimseyi bulamıyordu. Devre arasında Mete, takım arkadaşlarını etrafına topladı. "Arkadaşlar," dedi. "Hepimiz en iyi olduğumuz şeyi yapalım ama bunu birbirimiz için yapalım. Selin sen hızınla topu taşı, Can sen ribaundları al ve bana pas at, ben de en uygun anı bekleyeyim."

İkinci yarıda bambaşka bir takım vardı sahada. Artık kimse tek başına kahraman olmaya çalışmıyordu. Selin topu kaptığında hemen boşta olan arkadaşına bakıyor, Can pota altında devleşiyor, Mete ise aldığı pasları dikkatle değerlendiriyordu. Kenarda oturan yedek arkadaşlarının alkışları ve tezahüratları onlara güç veriyordu.

Maç bittiğinde skor tahtasında Mete'nin takımı öndeydi. Ama en güzeli, maç sonunda iki takımın da birbirini tebrik etmesiydi. Mete ve arkadaşları madalyalarını alırken şunu fark ettiler: En büyük yetenek, farklı yetenekleri bir araya getirip bir takım olabilmekti. O gün sadece maçı değil, "biz" olmayı başardıkları için hepsi gerçek birer şampiyondu."""},
       
        68: {"title": "68. Okuma Parçası: Rengarenk Kanatlar", "content":"""Baharın gelişiyle birlikte orman, adeta uykusundan uyanmış gibiydi. Küçük Beril, bahçedeki dut ağacının yaprakları arasında gezinen yeşil, tombul bir tırtıl gördü. Tırtıl büyük bir iştahla yaprakları yiyor, ağır ağır ilerliyordu. Beril, "Bu minik dostumuz ne kadar da yavaş hareket ediyor," diye düşündü.

Aradan günler geçti. Beril tekrar ağacın yanına gittiğinde tırtılın orada olmadığını, onun yerine dalda asılı duran sert, grimsi bir koza gördü. Babası ona, "Sabret Beril," dedi. "Doğa büyük bir hazırlık içinde. Tırtıl şimdi kendi ördüğü bu küçük evde dinleniyor ve mucizevi bir değişime hazırlanıyor."

Bir sabah güneşin ilk ışıklarıyla birlikte koza çatlamaya başladı. Beril nefesini tutmuş izliyordu. Kozanın içinden önce ince bacaklar, sonra da ıslak ve buruşuk kanatlar çıktı. Bu, o eski tombul tırtılın ta kendisiydi ama artık bambaşka görünüyordu! Kanatları kuruyup açıldıkça üzerindeki renkler parlamaya başladı. Turuncular, maviler ve siyah benekler... Az önce yürümekte zorlanan canlı, şimdi gökyüzüne doğru süzülmeye hazırdı.

Kelebek, kanatlarını birkaç kez çırptı ve bahçedeki çiçeklere doğru uçtu. Beril, kelebeğin çiçekten çiçeğe konarken kanatlarının nasıl da bir gökkuşağı gibi parladığını fark etti. Her kanat çırpışında doğanın güzelliğini her yere taşıyor gibiydi.

O gün Beril, hayatta her güzel şeyin bir zamanı ve bir hazırlık süreci olduğunu öğrendi. Tırtılın sabrı, ona dünyanın en renkli kanatlarını kazandırmıştı. Kelebekler sadece uçan renkler değil, aynı zamanda doğanın bize sunduğu en zarif başarı hikayeleriydi. Beril, renk renk kelebeklerin peşinden koştururken, doğanın her köşesinde keşfedilmeyi bekleyen bir mucize olduğunu biliyordu."""},
       
        69: {"title": "69. Okuma Parçası: Mektup Arkadaşım", "content":"""Nil, o sabah postacının yolunu her zamankinden daha büyük bir heyecanla gözlüyordu. Çünkü bugün, Türkiye’nin en doğusundaki Kars’ta yaşayan mektup arkadaşı Yusuf’tan haber bekliyordu. Nil ve Yusuf hiç tanışmamışlardı ama bir okul projesi sayesinde birbirlerine mektup yazmaya başlamışlardı.

Kısa süre sonra kapı çaldı. Gelen postacı amca, üzerinde Nil’in adının yazılı olduğu, köşesinde renkli pullar bulunan o zarfı uzattı. Nil, odasına koşup zarfı özenle açtı. İçinden Yusuf’un düzgün el yazısıyla yazılmış bir kağıt ve kurumuş bir çiçek çıktı.

Yusuf mektubunda, Kars’ın dondurucu soğuklarını, her sabah karla kaplanan sokakları ve okullarına giderken geçtikleri o eski taş köprüyü anlatıyordu. Nil, satırları okurken kendini sanki oradaymış gibi hissetti. Yusuf, "Buralar bembeyaz bir masal diyarı gibi Nil," diye yazmıştı. "Senin yaşadığın o sıcak Ege kasabası, denizin mavisi ve zeytin ağaçları kim bilir ne kadar güzeldir."

Nil, mektup yazmanın dijital mesajlardan ne kadar farklı olduğunu o an bir kez daha anladı. Bir mesaj saniyeler içinde gidiyordu ama bir mektubu beklemek, onun yolculuğunu hayal etmek ve kağıdın kokusunu içine çekmek bambaşka bir duyguydu. Mektuplar, insanların birbirine sadece kelimelerini değil, zamanlarını ve emeklerini de gönderdiği özel hediyelerdi.

Hemen masasına oturdu, en sevdiği kalemini eline aldı. Yusuf’a anlatacak çok şeyi vardı: Bahçelerinde açan ilk papatyaları, hafta sonu gittikleri deniz kenarını ve mektubuna eklemek için çektiği bir fotoğrafı hazırladı. "Sevgili Yusuf," diye başladı. Kalemi kağıdın üzerinde dans ederken, Nil uzakların aslında göründüğü kadar uzak olmadığını fark etti. Mektuplar sayesinde iki farklı şehir, iki farklı hayat, bembeyaz bir kağıt üzerinde birleşiyordu."""},
       
        70: {"title": "70. Okuma Parçası: Kütüphanede Bir Masa", "content":"""Okulun en sevdiğim köşesi, koridorun sonundaki o büyük ahşap kapının ardındaydı. Kapıyı yavaşça araladığınızda sizi karşılayan o eşsiz kitap kokusu, sanki binlerce maceranın aynı anda fısıldadığı bir davet gibiydi. Burası bizim okul kütüphanemizdi.

Ömer, o gün ödevi için güneş sistemi hakkında araştırma yapmaya karar vermişti. Kütüphaneye girdiğinde parmak uçlarında yürüyerek pencere kenarındaki boş bir masaya yerleşti. Kütüphanede her masanın kendine has bir hikayesi vardı. Bazı masalar matematik problemlerinin çözüldüğü ciddi yerler, bazıları ise masal kitaplarının heyecanla okunduğu hayal duraklarıydı.

Ömer, rafların arasında dolaşırken "Uzay ve Gezegenler" yazan bölüme ulaştı. Büyük, renkli bir ansiklopediyi alıp masasına geri döndü. Kütüphanede çalışmanın en güzel yanı sessizlikti. Sadece çevrilen sayfaların hışırtısı ve dışarıdaki kuşların cıvıltısı duyuluyordu. Bu sessizlik, insanın okuduğu şeye çok daha iyi odaklanmasını sağlıyordu.

Masasının üzerindeki lambayı açtı ve gezegenlerin büyüleyici dünyasına daldı. Satürn’ün halkalarını incelerken zamanın nasıl geçtiğini anlamamıştı. Kütüphanedeki o masa, Ömer için artık sadece bir mobilya değil; onu dünyadan alıp uzayın derinliklerine götüren bir uzay gemisi gibiydi.

Çalışmasını bitirdiğinde kitabını aldığı rafa özenle yerleştirdi. Masasını temiz bıraktı ve sandalyesini sessizce yerine itti. Çünkü kütüphanede paylaşılan sadece kitaplar değil, aynı zamanda ortak bir düzendi. Ömer, kütüphane kapısından çıkarken bir sonraki hafta hangi masaya oturup hangi yeni dünyayı keşfedeceğini şimdiden düşünmeye başlamıştı."""},
       
        71: {"title": "71. Okuma Parçası: Tarihi Kırmızı Tramvay", "content":"""İstanbul’un en canlı caddesi olan İstiklal Caddesi’nde, kalabalığın arasından nazlı bir gelin gibi süzülen, parıl parıl parlayan bir araç vardır. Rengi kıpkırmızı, sesi ise neşeli bir "çın çın"dır. Bu, şehrin en yaşlı ama en sevilen dostu olan tarihi kırmızı tramvaydır.

Küçük Ufuk, hafta sonu dedesiyle birlikte bu tarihi araca binmek için sabırsızlanıyordu. Tramvay durağa yanaştığında, Ufuk onun ahşap koltuklarına ve pirinçten yapılmış tutacaklarına hayranlıkla baktı. Dedesi gülümseyerek yanına oturdu. "Biliyor musun Ufuk," dedi dedesi, "Ben senin yaşındayken de bu tramvay burada çalışıyordu. O zamanlar şehirde bu kadar çok araba yoktu. İnsanlar bir yerden bir yere gitmek için hep bu kırmızı dostu beklerlerdi."

Tramvay yavaşça hareket etmeye başladı. Rayların üzerinden gelen ritmik sesler, sanki geçmişten gelen bir masalı anlatıyor gibiydi. Ufuk pencereden dışarı baktığında, caddedeki insanların durup tramvaya el salladığını gördü. Kırmızı tramvay sadece bir ulaşım aracı değil, aynı zamanda şehrin gülen yüzüydü. Modern metrolar ve hızlı otobüsler her yeri sarmış olsa da, bu kırmızı tramvay sabırla ve neşeyle yoluna devam ediyordu.

Yolculuk sırasında vatman amca, o meşhur çanı çalarak yayaları nazikçe uyarıyordu. Ufuk, "Dede," dedi, "Bu tramvay hiç yorulmuyor mu?" Dedesi cevap verdi: "O, şehrin hafızasıdır Ufuk. Biz ona iyi baktığımız sürece, o da bize eski günlerin güzelliğini hatırlatmaya devam edecek."

İstiklal Caddesi’nin sonuna geldiklerinde Ufuk, bu kırmızı dostundan ayrılmak istemedi. O gün anlamıştı ki; bazı şeyler eskise bile değerini asla kaybetmez. Kırmızı tramvay, raylar üzerinde giden basit bir vagon değil; dedesinin çocukluğu ile Ufuk’un hayallerini birbirine bağlayan sihirli bir köprüydü."""},

        72: {"title": "72. Okuma Parçası: Ara Bul Macerası", "content":"""Ekin ve Eylül, o gün okulun bahçesinde gizemli bir oyuna başladılar. Öğretmenleri onlara elindeki listeyi uzatırken gülümseyerek şöyle demişti: "Bugün sıradan bir teneffüs değil, bir keşif zamanı! Bahçede saklı olan bu detayları ilk bulan grup, 'Günün Dikkatli Gözleri' madalyasını alacak."

Listenin en başında ilginç bir madde vardı: "Gövdesinde gülen bir yüze benzeyen budak izi olan ağaç." Ekin hemen en büyük çınar ağacına koştu. Eğilip kalktı, gövdeyi bir büyüteçle inceler gibi süzdü. "Burada!" diye bağırdı. Gerçekten de ağacın gövdesindeki bir kabuk çatlağı, sanki onlara gülümsüyordu. Dikkatli bakmadıkça görülmeyecek bir ayrıntıydı bu.

Eylül ise ikinci maddeye odaklanmıştı: "Üzerinde yedi tane nokta olan minik bir misafir." Taşların arasına, yaprakların altına baktı. Tam umudunu kesecekken yeşil bir yaprağın üzerinde dinlenen bir uğur böceği gördü. "Ekin, buldum! İşte burada!" dedi. İki arkadaş, detayları fark etmenin ne kadar eğlenceli olduğunu anladılar. Dünya, dikkatli bakınca aslında kocaman bir oyun alanına dönüşüyordu.

Oyunun sonunda listedeki her şeyi bulmuşlardı: Üç farklı renkte taş, kalp şeklinde bir yaprak ve toprağın altına yuva yapan karıncaların giriş kapısı... Eylül, "Daha önce bu bahçede her gün yürüyorduk ama karıncaların kapısını hiç fark etmemiştim," dedi.

Öğretmenleri yanlarına geldiğinde ikisi de heyecanla bulduklarını anlattılar. "Çocuklar," dedi öğretmenleri, "Bakmak ile görmek farklıdır. Siz bugün sadece bakmadınız, aynı zamanda gördünüz. Dikkatli bir göz, dünyadaki tüm gizli güzellikleri bulabilir." Eylül ve Ekin o gün madalyalarını aldılar ama en büyük ödülleri, çevrelerine daha meraklı gözlerle bakmayı öğrenmek olmuştu. Artık her yolculuk, onlar için yeni bir "Ara Bul" macerasıydı."""},
        }
        
        for i in range(4, 73):
            if i not in self.library_source:
                self.library_source[i] = {
                    "title": f"Metin {i}: Görsel Algı Geliştirme",
                    "content": f"Bu {i}. seviye metni, göz kaslarınızı güçlendirmek için tasarlanmıştır. Düzenli okuma yaparak göz hareketlerinizi geliştirebilir ve görsel algınızı artırabilirsiniz."
                }

        self.data = self.load_data()
        self.lock_data = self.load_lock_data()
        self.weekly_data = self.load_weekly_data()

    def load_data(self):
        default_structure = {
            "session_current": 1,
            "completed_periods": 0,
            "unlocked_text_index": 1,
            "completed_texts_total": 0,
            "weekly_counter": 0,
            "last_session_time": None,
            "last_successful_session": 0,
            "current_session_status": "pending",
            "current_session_number": 1,
            "session_history": {},
            "session_texts": {},
            "settings": {
                "font_size": 24, 
                "brightness": 1.0, 
                "theme_mode": "gece"
            }
        }
        
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for key, val in default_structure.items():
                        if key not in data: 
                            data[key] = val
                    return data
            except Exception as e:
                print(f"Veri yüklenirken hata: {e}")
                return default_structure
        return default_structure

    def load_lock_data(self):
        default_lock = {
            "locks": {},
            "active_locks": []
        }
        
        if os.path.exists(self.lock_file):
            try:
                with open(self.lock_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if "locks" not in data:
                        data["locks"] = {}
                    if "active_locks" not in data:
                        data["active_locks"] = []
                    return data
            except:
                return default_lock
        return default_lock

    def load_weekly_data(self):
        default_weekly = {
            "current_week_start": None,
            "sessions_completed_this_week": 0,
            "last_week_reset": None,
            "total_weeks": 0
        }
        
        if os.path.exists(self.weekly_file):
            try:
                with open(self.weekly_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return default_weekly
        return default_weekly

    def save_data(self):
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def save_lock_data(self):
        with open(self.lock_file, "w", encoding="utf-8") as f:
            json.dump(self.lock_data, f, indent=4, ensure_ascii=False)

    def save_weekly_data(self):
        with open(self.weekly_file, "w", encoding="utf-8") as f:
            json.dump(self.weekly_data, f, indent=4, ensure_ascii=False)

    def set_session_lock(self, completed_session_number):
        """Başarıyla tamamlanan seans için bir sonraki seansı 36 saat kitle"""
        now = datetime.now()
        next_session = completed_session_number + 1
        
        # Eğer zaten kilit varsa, yenileme
        if str(next_session) in self.lock_data["locks"]:
            lock_data = self.lock_data["locks"][str(next_session)]
            lock_until = datetime.fromtimestamp(lock_data["locked_until"])
            
            # Eğer kilit süresi dolmuşsa veya dolmak üzereyse, yeni kilit oluştur
            if now >= lock_until - timedelta(seconds=10):
                lock_until = now + timedelta(hours=36)
                lock_data = {
                    "locked_at": datetime.timestamp(now),
                    "locked_until": datetime.timestamp(lock_until),
                    "iso_locked_until": lock_until.isoformat(),
                    "completed_session": completed_session_number
                }
                self.lock_data["locks"][str(next_session)] = lock_data
        else:
            # Yeni kilit oluştur
            lock_until = now + timedelta(hours=36)
            
            lock_data = {
                "locked_at": datetime.timestamp(now),
                "locked_until": datetime.timestamp(lock_until),
                "iso_locked_until": lock_until.isoformat(),
                "completed_session": completed_session_number
            }
            
            self.lock_data["locks"][str(next_session)] = lock_data
        
        self.update_active_locks()
        self.save_lock_data()

    def is_session_locked(self, session_number):
        """Belirli bir seans kilitli mi? - DÜZELTİLDİ: Mevcut ve başarısız seanslar kilitlenmez"""
        if session_number == 1:
            return False
        
        # ÖNEMLİ: Mevcut seans asla kilitli olmamalı
        current_session = self.get_current_session_number()
        session_status = self.get_current_session_status()
        
        # Mevcut seans veya başarısız seans kilitli değil
        if session_number == current_session:
            return False
        
        # Gelecekteki seanslar için kilit kontrolü
        session_key = str(session_number)
        if session_key not in self.lock_data["locks"]:
            return False
        
        lock_data = self.lock_data["locks"][session_key]
        now = datetime.timestamp(datetime.now())
        locked_until = lock_data.get("locked_until", 0)
        
        if now < locked_until:
            return True
        else:
            # Süre dolmuşsa kilidi kaldır
            del self.lock_data["locks"][session_key]
            self.update_active_locks()
            self.save_lock_data()
            return False

    def get_remaining_lock_time(self, session_number=None):
        """Kilit için kalan süreyi hesapla"""
        if session_number is None:
            if not self.lock_data.get("active_locks"):
                return "00:00:00"
            next_locked_session = min(self.lock_data["active_locks"])
            return self.get_remaining_lock_time(next_locked_session)
        
        session_key = str(session_number)
        if session_key not in self.lock_data["locks"]:
            return "00:00:00"
        
        lock_data = self.lock_data["locks"][session_key]
        now = datetime.timestamp(datetime.now())
        locked_until = lock_data.get("locked_until", 0)
        
        if now >= locked_until:
            del self.lock_data["locks"][session_key]
            self.update_active_locks()
            self.save_lock_data()
            return "00:00:00"
        
        remaining = locked_until - now
        hours = int(remaining // 3600)
        minutes = int((remaining % 3600) // 60)
        seconds = int(remaining % 60)
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def update_active_locks(self):
        """Aktif kilitleri güncelle"""
        now = datetime.timestamp(datetime.now())
        active_locks = []
        
        for session_key, lock_data in self.lock_data["locks"].items():
            locked_until = lock_data.get("locked_until", 0)
            if now < locked_until:
                active_locks.append(int(session_key))
        
        self.lock_data["active_locks"] = sorted(active_locks)
        self.save_lock_data()

    def update_weekly_tracking(self):
        """Haftalık takip verilerini güncelle"""
        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
        week_start_timestamp = datetime.timestamp(week_start)
        
        if self.weekly_data["current_week_start"] is None:
            self.weekly_data["current_week_start"] = week_start_timestamp
            self.weekly_data["sessions_completed_this_week"] = 0
        elif week_start_timestamp != self.weekly_data["current_week_start"]:
            self.weekly_data["current_week_start"] = week_start_timestamp
            self.weekly_data["sessions_completed_this_week"] = 0
            self.weekly_data["total_weeks"] += 1
        
        self.weekly_data["sessions_completed_this_week"] += 1
        self.save_weekly_data()

    def get_weekly_stats(self):
        """Haftalık istatistikleri getir"""
        now = datetime.now()
        
        if self.weekly_data["current_week_start"]:
            week_start = datetime.fromtimestamp(self.weekly_data["current_week_start"])
            days_passed = (now - week_start).days + 1
            current_day = days_passed
            
            return {
                "completed": self.weekly_data["sessions_completed_this_week"],
                "target": 3,
                "day": current_day
            }
        else:
            return {
                "completed": 0,
                "target": 3,
                "day": 1
            }

    def reset_lock(self):
        self.lock_data = {
            "locks": {},
            "active_locks": []
        }
        self.save_lock_data()

    def reset_progress(self):
        saved_settings = self.data.get("settings", {
            "font_size": 24, 
            "brightness": 1.0, 
            "theme_mode": "gece"
        })
        
        self.data = {
            "session_current": 1, 
            "completed_periods": 0, 
            "unlocked_text_index": 1,
            "completed_texts_total": 0, 
            "weekly_counter": 0, 
            "last_session_time": None,
            "last_successful_session": 0,
            "current_session_status": "pending",
            "current_session_number": 1,
            "session_history": {},
            "session_texts": {},
            "settings": saved_settings
        }
        self.save_data()
        self.reset_lock()
        
        self.weekly_data = {
            "current_week_start": None,
            "sessions_completed_this_week": 0,
            "last_week_reset": datetime.now().isoformat(),
            "total_weeks": 0
        }
        self.save_weekly_data()

    def get_text(self, text_id): 
        return self.library_source.get(
            text_id, 
            {
                "title": f"Metin {text_id}", 
                "content": f"Metin {text_id} içeriği yükleniyor..."
            }
        )

    def get_setting(self, key): 
        return self.data["settings"].get(key)

    def set_setting(self, key, value):
        self.data["settings"][key] = value
        self.save_data()

    def get_current_session_number(self):
        """Mevcut seans numarasını hesapla"""
        return self.data["current_session_number"]

    def can_access_text(self, text_id):
        """Metin erişim kontrolü - TAMAMEN YENİDEN DÜZENLENDİ"""
        # Metin hangi seansa ait?
        text_session = (text_id + 1) // 2
        current_session = self.get_current_session_number()
        last_successful = self.data["last_successful_session"]
        session_status = self.get_current_session_status()
        
        # 1. Eğer bu seans tamamlanmışsa, tüm metinler açık
        if text_session <= last_successful:
            return True
        
        # 2. Mevcut seans
        if text_session == current_session:
            # Mevcut seansta sadece unlock edilmiş metinlere erişim
            return text_id <= self.data["unlocked_text_index"]
        
        # 3. Gelecekteki seanslar - sadece kilidi açıksa
        if text_session > current_session:
            # Bir sonraki seansa erişim için mevcut seansın başarılı olması gerekir
            if text_session == current_session + 1:
                if last_successful >= current_session:
                    # 36 saatlik kilit kontrolü
                    return not self.is_session_locked(text_session)
                else:
                    return False
            else:
                # Daha ileri seanslara erişim yok
                return False
        
        # 4. Geçmişteki seanslar - erişim var
        if text_session < current_session:
            return True
        
        return False

    def complete_text(self, text_id):
        """Metin tamamlandığında çağrılır"""
        # Sadece sıradaki metin tamamlanabilir
        if text_id == self.data["unlocked_text_index"]:
            self.data["unlocked_text_index"] += 1
            self.data["completed_texts_total"] += 1
            
            # Bu seans için metinleri kaydet
            session_num = self.get_current_session_number()
            session_key = str(session_num)
            
            if "session_texts" not in self.data:
                self.data["session_texts"] = {}
            
            if session_key not in self.data["session_texts"]:
                self.data["session_texts"][session_key] = []
            
            if text_id not in self.data["session_texts"][session_key]:
                self.data["session_texts"][session_key].append(text_id)
            
            self.save_data()
            return True
        return False

    def start_session(self):
        """2 metin tamamlandığında seansı başlat"""
        self.data["current_session_status"] = "active"
        self.save_data()
        return True

    def complete_session(self, success):
        """Seans tamamlama işlemi - DÜZELTİLDİ: Sadece başarılı seanslardan sonra kilit"""
        current_session = self.get_current_session_number()
        
        if success:
            # BAŞARILI - EGZERSİZ TAMAMLANDI
            self.data["last_successful_session"] = current_session
            self.data["current_session_status"] = "completed"
            
            # ÖNEMLİ: SADECE BAŞARILI SEANSLARDAN SONRA BİR SONRAKİ SEANSI KİLİTLE
            next_session = current_session + 1
            self.set_session_lock(current_session)
            
            # Haftalık takibi güncelle
            self.update_weekly_tracking()
            
            # Bir sonraki seans için hazırlık
            self.data["current_session_number"] = next_session
            self.data["current_session_status"] = "pending"
            
            # Yeni seans için unlocked_text_index'i ayarla
            # Her seans 2 metin: (seans * 2) - 1 ve (seans * 2)
            next_session_first_text = (next_session * 2) - 1
            self.data["unlocked_text_index"] = next_session_first_text
            
        else:
            # BAŞARISIZ - EGZERSİZ YARIDA KALDI
            self.data["current_session_status"] = "failed"
            
            # BAŞARISIZ DURUMDA:
            # 1. unlocked_text_index DEĞİŞMEZ - aynı kalır
            # 2. current_session_number DEĞİŞMEZ - aynı seans kalır
            # 3. Kullanıcı aynı seansa devam edebilir
            # 4. KİLİT OLUŞTURULMAZ - sonraki seans kilitlenmez
        
        # Geçmişe kaydet
        if "session_history" not in self.data:
            self.data["session_history"] = {}
        
        session_key = str(current_session)
        texts_completed = len(self.data["session_texts"].get(session_key, []))
        
        self.data["session_history"][session_key] = {
            "completed_at": datetime.now().isoformat(),
            "success": success,
            "texts_completed": texts_completed
        }
        
        self.save_data()
        return success

    def get_session_completion_time(self, session_number):
        """Belirli bir seansın tamamlanma zamanını getir"""
        session_key = str(session_number)
        if session_key in self.lock_data["locks"]:
            lock_data = self.lock_data["locks"][session_key]
            locked_at = lock_data.get("locked_at")
            if locked_at:
                return datetime.fromtimestamp(locked_at)
        return None

    def get_next_locked_session(self):
        """Bir sonraki kilitli seansı bul"""
        if not self.lock_data.get("active_locks"):
            return None
        
        current_session = self.get_current_session_number()
        
        for session in sorted(self.lock_data["active_locks"]):
            if session > current_session:
                return session
        
        return None

    def get_current_session_status(self):
        """Mevcut seansın durumunu getir"""
        return self.data.get("current_session_status", "pending")

    def can_retry_exercise(self):
        """Başarısız seans durumunda egzersizi yeniden deneyebilir mi?"""
        current_session = self.get_current_session_number()
        session_status = self.get_current_session_status()
        
        # Seans başarısızsa ve 2 metin tamamlanmışsa egzersiz yeniden denenebilir
        if session_status == "failed":
            # Bu seans için tamamlanan metin sayısını kontrol et
            session_key = str(current_session)
            texts_completed = len(self.data["session_texts"].get(session_key, []))
            return texts_completed >= 2
        
        return False

    def get_session_text_range(self, session_number):
        """Belirli bir seansın metin aralığını getir"""
        first_text = (session_number * 2) - 1
        last_text = session_number * 2
        return first_text, last_text