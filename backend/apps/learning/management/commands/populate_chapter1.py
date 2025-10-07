from django.core.management.base import BaseCommand
from apps.learning.models import Subject, SubjectItem, Chapter, Page, TextBlock, VocabularyEntry, QuizQuestion, QuizOption


class Command(BaseCommand):
    help = 'Populate Chapter 1 (介護保険制度とは？) with existing text content'

    def handle(self, *args, **options):
        self.stdout.write('Starting to populate Chapter 1 data...')

        # Get or create the hierarchy
        subject, _ = Subject.objects.get_or_create(
            name='介護試験対策',
            defaults={'indonesian_name': 'Persiapan Ujian Kaigo', 'order': 1}
        )

        item, _ = SubjectItem.objects.get_or_create(
            subject=subject,
            name='介護保険',
            defaults={'order': 1}
        )

        chapter, _ = Chapter.objects.get_or_create(
            item=item,
            name='第1章',
            defaults={'description': '1. 介護保険制度とは？', 'order': 1}
        )

        page, _ = Page.objects.get_or_create(
            chapter=chapter,
            name='1. 介護保険制度とは？',
            defaults={'order': 1}
        )

        self.stdout.write(f'Created/found: {page}')

        # Clear existing data for this page to avoid duplicates
        TextBlock.objects.filter(page=page).delete()
        QuizQuestion.objects.filter(page=page).delete()

        # Text Block 1
        text_block_1 = TextBlock.objects.create(
            page=page,
            japanese_text='介護保険制度は、高齢者の介護を社会全体で支える仕組みです。',
            indonesian_translation='Sistem asuransi perawatan jangka panjang adalah mekanisme untuk mendukung perawatan lansia oleh seluruh masyarakat.',
            order=1
        )

        vocab_data_1 = [
            ('介護保険制度', 'Sistem asuransi perawatan jangka panjang'),
            ('高齢者', 'Lansia'),
            ('介護', 'Perawatan'),
            ('社会全体', 'Seluruh masyarakat'),
            ('支える', 'Mendukung'),
            ('仕組み', 'Mekanisme / Sistem'),
        ]

        for idx, (jp, indo) in enumerate(vocab_data_1, 1):
            VocabularyEntry.objects.create(
                text_block=text_block_1,
                japanese_word=jp,
                indonesian_translation=indo,
                order=idx
            )

        # Text Block 2
        text_block_2 = TextBlock.objects.create(
            page=page,
            japanese_text='40歳以上の国民が保険料を納め、介護が必要になったときに、費用の一部を負担するだけで様々なサービスを利用できます。',
            indonesian_translation='Warga negara berusia 40 tahun ke atas membayar premi asuransi, dan ketika perawatan diperlukan, mereka dapat menggunakan berbagai layanan hanya dengan menanggung sebagian dari biayanya.',
            order=2
        )

        vocab_data_2 = [
            ('40歳以上', 'Berusia 40 tahun ke atas'),
            ('国民', 'Warga negara'),
            ('保険料', 'Premi asuransi'),
            ('納め', 'Membayar'),
            ('介護', 'Perawatan'),
            ('必要に', 'diperlukan'),
            ('費用', 'Biaya'),
            ('一部', 'Sebagian'),
            ('負担する', 'Menanggung'),
            ('様々', 'Berbagai macam'),
            ('サービス', 'Layanan'),
            ('利用できます', 'Dapat menggunakan'),
        ]

        for idx, (jp, indo) in enumerate(vocab_data_2, 1):
            VocabularyEntry.objects.create(
                text_block=text_block_2,
                japanese_word=jp,
                indonesian_translation=indo,
                order=idx
            )

        # Text Block 3
        text_block_3 = TextBlock.objects.create(
            page=page,
            japanese_text='運営の主体（保険者）→ 市町村と特別区です。',
            indonesian_translation='Badan penyelenggara (penanggung) → Pemerintah kota dan distrik khusus.',
            order=3
        )

        vocab_data_3 = [
            ('運営の主体', 'Badan penyelenggara'),
            ('保険者', 'Penanggung (asuransi)'),
            ('市町村', 'Pemerintah kota'),
            ('特別区', 'Distrik khusus'),
        ]

        for idx, (jp, indo) in enumerate(vocab_data_3, 1):
            VocabularyEntry.objects.create(
                text_block=text_block_3,
                japanese_word=jp,
                indonesian_translation=indo,
                order=idx
            )

        # Text Block 4
        text_block_4 = TextBlock.objects.create(
            page=page,
            japanese_text='目的→ 高齢者が尊厳を保ち、能力に応じて自立した日常生活を送れるように支援することです。',
            indonesian_translation='Tujuan → Untuk mendukung lansia agar dapat mempertahankan martabat mereka dan menjalani kehidupan sehari-hari yang mandiri sesuai dengan kemampuan mereka.',
            order=4
        )

        vocab_data_4 = [
            ('目的', 'Tujuan'),
            ('高齢者', 'Lansia'),
            ('尊厳', 'Martabat'),
            ('保ち', 'Menjaga'),
            ('能力', 'Kemampuan'),
            ('応じて', 'Sesuai dengan'),
            ('自立した', 'Mandiri'),
            ('日常生活', 'Kehidupan sehari-hari'),
            ('送れるよう', 'Agar dapat menjalani'),
            ('支援する', 'Mendukung'),
        ]

        for idx, (jp, indo) in enumerate(vocab_data_4, 1):
            VocabularyEntry.objects.create(
                text_block=text_block_4,
                japanese_word=jp,
                indonesian_translation=indo,
                order=idx
            )

        self.stdout.write(self.style.SUCCESS(f'Created {TextBlock.objects.filter(page=page).count()} text blocks'))
        self.stdout.write(self.style.SUCCESS(f'Created {VocabularyEntry.objects.filter(text_block__page=page).count()} vocabulary entries'))

        # Quiz Question 1
        question_1 = QuizQuestion.objects.create(
            page=page,
            question_number=1,
            question_text='介護保険制度の目的として、最も適切なものはどれか？',
            order=1
        )

        quiz_1_options = [
            (1, '高齢者の医療費を軽減すること', False,
             '医療費の軽減は医療保険の目的です。介護保険は介護に要する費用の支援が目的です。',
             'Mengurangi biaya medis adalah tujuan asuransi kesehatan. Tujuan asuransi perawatan jangka panjang adalah untuk mendukung biaya yang diperlukan untuk perawatan.'),
            (2, '高齢者が尊厳を保ち、自立した生活を送れるよう支援すること', True,
             '正解です。介護保険法第1条に定められている目的です。単に介護するだけでなく、利用者の尊厳と自立支援が重視されます。',
             'Benar. Ini adalah tujuan yang ditetapkan dalam Pasal 1 Undang-Undang Asuransi Perawatan Jangka Panjang. Tidak hanya sekadar merawat tetapi juga menekankan dukungan terhadap martabat dan kemandirian pengguna.'),
            (3, '介護施設の数を増やすこと', False,
             '介護基盤の整備は重要ですが、制度の直接的な目的ではありません。目的を達成するための手段の一つです。',
             'Pengembangan infrastruktur perawatan memang penting tetapi itu bukan tujuan langsung dari sistem ini. Itu adalah salah satu cara untuk mencapai tujuan.'),
            (4, '家族の介護負担を完全になくすこと', False,
             '家族の負担軽減も制度の重要な役割ですが、「完全になくすこと」が目的ではありません。社会全体で支えることが基本です。',
             'Mengurangi beban keluarga juga merupakan peran penting dari sistem ini tetapi tujuannya bukan untuk \'menghilangkannya sepenuhnya\'. Prinsip dasarnya adalah dukungan dari seluruh masyarakat.'),
            (5, '40歳以上の国民全員に介護サービスを提供すること', False,
             'サービスが提供されるのは、保険料を納めている人のうち、介護が必要だと認定された人です。全員ではありません。',
             'Layanan diberikan kepada mereka yang membayar premi dan telah disertifikasi membutuhkan perawatan. Tidak untuk semua orang.'),
        ]

        for opt_num, opt_text, is_correct, exp_jp, exp_indo in quiz_1_options:
            QuizOption.objects.create(
                question=question_1,
                option_number=opt_num,
                option_text=opt_text,
                is_correct=is_correct,
                explanation_japanese=exp_jp,
                explanation_indonesian=exp_indo
            )

        # Quiz Question 2
        question_2 = QuizQuestion.objects.create(
            page=page,
            question_number=2,
            question_text='介護保険制度の保険者（運営の主体）として、正しいものはどれか？',
            order=2
        )

        quiz_2_options = [
            (1, '国', False,
             '国の役割は制度の基準設定や財政支援ですが、直接の運営主体ではありません。',
             'Peran negara adalah menetapkan standar sistem dan dukungan finansial tetapi bukan penyelenggara langsung.'),
            (2, '都道府県', False,
             '都道府県は、市町村への支援やサービス提供事業者の指定などを行いますが、保険者ではありません。',
             'Prefektur memberikan dukungan kepada pemerintah kota dan menunjuk penyedia layanan tetapi bukan penanggung.'),
            (3, '市町村と特別区', True,
             '正解です。介護保険は、住民に最も身近な行政単位である市町村と特別区が保険者として運営しています。',
             'Benar. Asuransi perawatan jangka panjang diselenggarakan oleh pemerintah kota dan distrik khusus yang merupakan unit administrasi terdekat dengan penduduk.'),
            (4, '医療保険組合', False,
             '医療保険組合は医療保険の運営主体であり、介護保険の運営主体とは異なります。',
             'Asosiasi asuransi kesehatan adalah penyelenggara asuransi kesehatan dan berbeda dari penyelenggara asuransi perawatan jangka panjang.'),
            (5, '後期高齢者医療広域連合', False,
             'これは後期高齢者医療制度の運営主体であり、介護保険の保険者ではありません。',
             'Ini adalah badan penyelenggara sistem asuransi kesehatan untuk lansia lanjutan bukan penanggung asuransi perawatan jangka panjang.'),
        ]

        for opt_num, opt_text, is_correct, exp_jp, exp_indo in quiz_2_options:
            QuizOption.objects.create(
                question=question_2,
                option_number=opt_num,
                option_text=opt_text,
                is_correct=is_correct,
                explanation_japanese=exp_jp,
                explanation_indonesian=exp_indo
            )

        self.stdout.write(self.style.SUCCESS(f'Created {QuizQuestion.objects.filter(page=page).count()} quiz questions'))
        self.stdout.write(self.style.SUCCESS(f'Created {QuizOption.objects.filter(question__page=page).count()} quiz options'))
        self.stdout.write(self.style.SUCCESS('Successfully populated Chapter 1 data!'))
