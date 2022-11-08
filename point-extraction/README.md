08.11.2022


Üst üste binen neslerin segmentasyonu için 3 özel adımdan oluşur;

1 - seed region/point extraction
2 - contour evidence extraction
3 - contour estimation


<p align="center">
  <img src="https://github.com/HasanBeratSoke/leaves-segmentation/point-extraction/roadmap.jpg" />
</p>


İlk aşamada her nesne için noktalar yada ona karşılık gelen bölgelerin çıkarılmasıdır. Merkezi noktalar, genellikle nesnenin iç kısımları yada üst üste binen nesneye gösterilmesine referans olabilir. Buradaki amaç noktalar sayesinde bir resimdeki nesnenin sayısını çıkartmaktır sonrasında ise geliştirerek segmentasyon yapılabilmektedir.


İkinci aşama ise, kontur çıkarımı yapmaktır. ilk aşamada çıkarılan noktaları kullanılarak herbir nesnenin gruplandırılmasını sağlar.


Son aşamada ise, önceki iki aşamanın çıktısında oluşan nesnein kesişimden oluşan boşlukları dolmak olacaktır.

