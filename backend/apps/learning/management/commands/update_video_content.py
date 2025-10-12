# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from apps.learning.models import Video


class Command(BaseCommand):
    help = 'Update video content with ruby annotations'

    def handle(self, *args, **options):
        # 1つ目の動画を更新（ルビ付き）
        video1 = Video.objects.get(id=1)
        video1.content = '''<div class="content-block">
<div class="japanese-text"><ruby>介護<rt>かいご</rt></ruby>とは、<ruby>高齢者<rt>こうれいしゃ</rt></ruby>や<ruby>障害者<rt>しょうがいしゃ</rt></ruby>の<ruby>日常生活<rt>にちじょうせいかつ</rt></ruby>を<ruby>支援<rt>しえん</rt></ruby>することです。</div>
<div class="translation-text">Kaigo adalah dukungan untuk kehidupan sehari-hari orang lanjut usia dan penyandang disabilitas.</div>
</div>

<div class="content-block">
<div class="japanese-text"><ruby>利用者<rt>りようしゃ</rt></ruby>の<ruby>尊厳<rt>そんげん</rt></ruby>を<ruby>守<rt>まも</rt></ruby>ることが<ruby>最<rt>もっと</rt></ruby>も<ruby>大切<rt>たいせつ</rt></ruby>です。</div>
<div class="translation-text">Melindungi martabat pengguna adalah yang paling penting.</div>
</div>

<div class="content-block">
<div class="japanese-text"><ruby>一人<rt>ひとり</rt></ruby>ひとりの<ruby>個性<rt>こせい</rt></ruby>や<ruby>価値観<rt>かちかん</rt></ruby>を<ruby>尊重<rt>そんちょう</rt></ruby>し、その<ruby>人<rt>ひと</rt></ruby>らしい<ruby>生活<rt>せいかつ</rt></ruby>を<ruby>支援<rt>しえん</rt></ruby>します。</div>
<div class="translation-text">Menghormati kepribadian dan nilai-nilai setiap orang, dan mendukung kehidupan yang sesuai dengan diri mereka.</div>
</div>

<div class="content-block">
<div class="japanese-text"><ruby>介護<rt>かいご</rt></ruby>の<ruby>基本<rt>きほん</rt></ruby>は、<ruby>移動<rt>いどう</rt></ruby>・<ruby>移乗<rt>いじょう</rt></ruby>、<ruby>食事<rt>しょくじ</rt></ruby>、<ruby>排泄<rt>はいせつ</rt></ruby>、<ruby>入浴<rt>にゅうよく</rt></ruby>などの<ruby>日常生活動作<rt>にちじょうせいかつどうさ</rt></ruby>（ADL）の<ruby>支援<rt>しえん</rt></ruby>です。</div>
<div class="translation-text">Dasar dari kaigo adalah dukungan untuk aktivitas kehidupan sehari-hari (ADL) seperti perpindahan, makan, buang air, dan mandi.</div>
</div>

<div class="content-block">
<div class="japanese-text">ボディメカニクスを<ruby>活用<rt>かつよう</rt></ruby>することで、<ruby>介護者<rt>かいごしゃ</rt></ruby>の<ruby>負担<rt>ふたん</rt></ruby>を<ruby>軽減<rt>けいげん</rt></ruby>し、<ruby>利用者<rt>りようしゃ</rt></ruby>にも<ruby>安全<rt>あんぜん</rt></ruby>な<ruby>介助<rt>かいじょ</rt></ruby>ができます。</div>
<div class="translation-text">Dengan menggunakan body mechanics, beban pada perawat dapat dikurangi dan bantuan yang aman dapat diberikan kepada pengguna.</div>
</div>

<div class="content-block">
<div class="japanese-text">コミュニケーションは<ruby>信頼関係<rt>しんらいかんけい</rt></ruby>を<ruby>築<rt>きず</rt></ruby>くために<ruby>欠<rt>か</rt></ruby>かせません。</div>
<div class="translation-text">Komunikasi sangat penting untuk membangun hubungan kepercayaan.</div>
</div>

<div class="content-block">
<div class="japanese-text"><ruby>傾聴<rt>けいちょう</rt></ruby>の<ruby>姿勢<rt>しせい</rt></ruby>で、<ruby>利用者<rt>りようしゃ</rt></ruby>の<ruby>話<rt>はなし</rt></ruby>をしっかりと<ruby>聞<rt>き</rt></ruby>くことが<ruby>大切<rt>たいせつ</rt></ruby>です。</div>
<div class="translation-text">Penting untuk mendengarkan cerita pengguna dengan seksama dengan sikap mendengarkan aktif.</div>
</div>'''
        video1.save()
        self.stdout.write(self.style.SUCCESS('動画1を更新（ルビ付き）'))

        # 2つ目の動画を更新（ルビ付き）
        video2 = Video.objects.get(id=2)
        video2.content = '''<div class="content-block">
<div class="japanese-text"><ruby>認知症<rt>にんちしょう</rt></ruby>は、<ruby>記憶障害<rt>きおくしょうがい</rt></ruby>を<ruby>中心<rt>ちゅうしん</rt></ruby>とした<ruby>認知機能<rt>にんちきのう</rt></ruby>の<ruby>低下<rt>ていか</rt></ruby>により、<ruby>日常生活<rt>にちじょうせいかつ</rt></ruby>に<ruby>支障<rt>ししょう</rt></ruby>をきたす<ruby>状態<rt>じょうたい</rt></ruby>です。</div>
<div class="translation-text">Demensia adalah kondisi di mana fungsi kognitif menurun, terutama gangguan memori, yang mengganggu kehidupan sehari-hari.</div>
</div>

<div class="content-block">
<div class="japanese-text">アルツハイマー<ruby>型認知症<rt>がたにんちしょう</rt></ruby>、<ruby>血管性認知症<rt>けっかんせいにんちしょう</rt></ruby>、レビー<ruby>小体型認知症<rt>しょうたいがたにんちしょう</rt></ruby>など、<ruby>様々<rt>さまざま</rt></ruby>なタイプがあります。</div>
<div class="translation-text">Ada berbagai jenis seperti demensia tipe Alzheimer, demensia vaskular, dan demensia dengan badan Lewy.</div>
</div>

<div class="content-block">
<div class="japanese-text">パーソンセンタードケアとは、<ruby>認知症<rt>にんちしょう</rt></ruby>の<ruby>方<rt>かた</rt></ruby>を<ruby>一人<rt>ひとり</rt></ruby>の<ruby>人<rt>ひと</rt></ruby>として<ruby>尊重<rt>そんちょう</rt></ruby>するケアの<ruby>考<rt>かんが</rt></ruby>え<ruby>方<rt>かた</rt></ruby>です。</div>
<div class="translation-text">Person-centered care adalah pendekatan perawatan yang menghormati orang dengan demensia sebagai individu.</div>
</div>

<div class="content-block">
<div class="japanese-text"><ruby>環境<rt>かんきょう</rt></ruby>を<ruby>整<rt>ととの</rt></ruby>えることで、<ruby>見当識<rt>けんとうしき</rt></ruby>を<ruby>保<rt>たも</rt></ruby>ち、<ruby>安全<rt>あんぜん</rt></ruby>で<ruby>落<rt>お</rt></ruby>ち<ruby>着<rt>つ</rt></ruby>ける<ruby>空間<rt>くうかん</rt></ruby>を<ruby>作<rt>つく</rt></ruby>ります。</div>
<div class="translation-text">Dengan mengatur lingkungan, kita dapat mempertahankan orientasi dan menciptakan ruang yang aman dan tenang.</div>
</div>

<div class="content-block">
<div class="japanese-text">ゆっくりと<ruby>分<rt>わ</rt></ruby>かりやすい<ruby>言葉<rt>ことば</rt></ruby>で<ruby>話<rt>はな</rt></ruby>し、<ruby>否定<rt>ひてい</rt></ruby>せず<ruby>共感<rt>きょうかん</rt></ruby>する<ruby>姿勢<rt>しせい</rt></ruby>が<ruby>大切<rt>たいせつ</rt></ruby>です。</div>
<div class="translation-text">Penting untuk berbicara dengan kata-kata yang mudah dipahami secara perlahan, dan memiliki sikap empati tanpa menyangkal.</div>
</div>

<div class="content-block">
<div class="japanese-text">BPSD（<ruby>行動<rt>こうどう</rt></ruby>・<ruby>心理症状<rt>しんりしょうじょう</rt></ruby>）には、<ruby>原因<rt>げんいん</rt></ruby>を<ruby>探<rt>さぐ</rt></ruby>り、<ruby>適切<rt>てきせつ</rt></ruby>に<ruby>対応<rt>たいおう</rt></ruby>することが<ruby>必要<rt>ひつよう</rt></ruby>です。</div>
<div class="translation-text">Untuk BPSD (gejala perilaku dan psikologis), perlu mencari penyebabnya dan merespons dengan tepat.</div>
</div>'''
        video2.save()
        self.stdout.write(self.style.SUCCESS('動画2を更新（ルビ付き）'))

        # 3つ目の動画を更新（ルビ付き）
        video3 = Video.objects.get(id=3)
        video3.content = '''<div class="content-block">
<div class="japanese-text"><ruby>食事<rt>しょくじ</rt></ruby>は<ruby>生活<rt>せいかつ</rt></ruby>の<ruby>楽<rt>たの</rt></ruby>しみの<ruby>一<rt>ひと</rt></ruby>つであり、<ruby>安全<rt>あんぜん</rt></ruby>で<ruby>快適<rt>かいてき</rt></ruby>な<ruby>食事時間<rt>しょくじじかん</rt></ruby>を<ruby>提供<rt>ていきょう</rt></ruby>することが<ruby>大切<rt>たいせつ</rt></ruby>です。</div>
<div class="translation-text">Makanan adalah salah satu kesenangan dalam hidup, dan penting untuk menyediakan waktu makan yang aman dan nyaman.</div>
</div>

<div class="content-block">
<div class="japanese-text"><ruby>介助者<rt>かいじょしゃ</rt></ruby>は<ruby>利用者<rt>りようしゃ</rt></ruby>と<ruby>同<rt>おな</rt></ruby>じ<ruby>目線<rt>めせん</rt></ruby>の<ruby>高<rt>たか</rt></ruby>さで、<ruby>横<rt>よこ</rt></ruby>または<ruby>斜<rt>なな</rt></ruby>め<ruby>前<rt>まえ</rt></ruby>から<ruby>介助<rt>かいじょ</rt></ruby>するのが<ruby>基本<rt>きほん</rt></ruby>です。</div>
<div class="translation-text">Dasar dari bantuan adalah perawat membantu dari samping atau diagonal depan pada ketinggian mata yang sama dengan pengguna.</div>
</div>

<div class="content-block">
<div class="japanese-text"><ruby>誤嚥<rt>ごえん</rt></ruby>を<ruby>防<rt>ふせ</rt></ruby>ぐために、<ruby>上体<rt>じょうたい</rt></ruby>を<ruby>起<rt>お</rt></ruby>こし、<ruby>顎<rt>あご</rt></ruby>を<ruby>引<rt>ひ</rt></ruby>いた<ruby>姿勢<rt>しせい</rt></ruby>で<ruby>食事<rt>しょくじ</rt></ruby>をします。</div>
<div class="translation-text">Untuk mencegah aspirasi, makan dengan postur tubuh bagian atas terangkat dan dagu ditarik ke dalam.</div>
</div>

<div class="content-block">
<div class="japanese-text"><ruby>足底<rt>そくてい</rt></ruby>が<ruby>床<rt>ゆか</rt></ruby>につく<ruby>安定<rt>あんてい</rt></ruby>した<ruby>座位<rt>ざい</rt></ruby>を<ruby>保<rt>たも</rt></ruby>つことが<ruby>重要<rt>じゅうよう</rt></ruby>です。</div>
<div class="translation-text">Penting untuk mempertahankan posisi duduk yang stabil dengan telapak kaki menyentuh lantai.</div>
</div>

<div class="content-block">
<div class="japanese-text"><ruby>一口量<rt>ひとくちりょう</rt></ruby>は<ruby>少<rt>すく</rt></ruby>なめにし、ゆっくりとしたペースで<ruby>介助<rt>かいじょ</rt></ruby>します。</div>
<div class="translation-text">Jumlah gigitan sedikit, dan bantu dengan kecepatan yang lambat.</div>
</div>

<div class="content-block">
<div class="japanese-text"><ruby>飲<rt>の</rt></ruby>み<ruby>込<rt>こ</rt></ruby>みを<ruby>確認<rt>かくにん</rt></ruby>してから、<ruby>次<rt>つぎ</rt></ruby>の<ruby>一口<rt>ひとくち</rt></ruby>を<ruby>運<rt>はこ</rt></ruby>びます。</div>
<div class="translation-text">Setelah mengonfirmasi menelan, berikan gigitan berikutnya.</div>
</div>

<div class="content-block">
<div class="japanese-text"><ruby>利用者<rt>りようしゃ</rt></ruby>の<ruby>咀嚼<rt>そしゃく</rt></ruby>・<ruby>嚥下機能<rt>えんげきのう</rt></ruby>に<ruby>合<rt>あ</rt></ruby>わせて、<ruby>食事形態<rt>しょくじけいたい</rt></ruby>を<ruby>調整<rt>ちょうせい</rt></ruby>することが<ruby>必要<rt>ひつよう</rt></ruby>です。</div>
<div class="translation-text">Perlu menyesuaikan bentuk makanan sesuai dengan fungsi mengunyah dan menelan pengguna.</div>
</div>

<div class="content-block">
<div class="japanese-text"><ruby>常食<rt>じょうしょく</rt></ruby>、<ruby>軟菜食<rt>なんさいしょく</rt></ruby>、<ruby>刻<rt>きざ</rt></ruby>み<ruby>食<rt>しょく</rt></ruby>、ペースト<ruby>食<rt>しょく</rt></ruby>など、<ruby>様々<rt>さまざま</rt></ruby>な<ruby>形態<rt>けいたい</rt></ruby>があります。</div>
<div class="translation-text">Ada berbagai bentuk seperti makanan biasa, makanan lunak, makanan cincang, dan makanan pasta.</div>
</div>'''
        video3.save()
        self.stdout.write(self.style.SUCCESS('動画3を更新（ルビ付き）'))

        self.stdout.write(self.style.SUCCESS('\n全ての動画にルビを追加しました！'))
