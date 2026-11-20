from tdk.home import HomepageContent


def test_homepage_content_from_new_widget_response():
    content = HomepageContent.model_validate(
        {
            "sayac": [{"deger": "1.2.3"}],
            "karistirma": [
                {
                    "id": 1,
                    "yanlis": "örnek yanlış",
                    "dogru": "örnek doğru",
                }
            ],
            "atasoz": [
                {"sozum": "örnek atasözü", "anlami": "örnek anlam"}
            ],
            "syyd": [
                {
                    "id": 2,
                    "yanliskelime": "örnek yanlış",
                    "dogrukelime": "örnek doğru",
                }
            ],
            "kural": [
                {"adi": "Örnek Kural", "url": "https://example.com"}
            ],
            "yabanci": {
                "karsid": 3,
                "kkelime": "örnek yabancı sözcük",
                "kkoken": "Örnekçe",
                "kkarsilik": "örnek karşılık",
                "anlam": "örnek anlam",
            },
            "kelime": [],
            "gundem": [
                {
                    "type": "gunun_kelimesi",
                    "madde": "örnek madde",
                    "anlam": "örnek anlam",
                }
            ],
        }
    )

    assert content.counter == (1, 2, 3)
    assert content.proverbs[0].proverb == "örnek atasözü"
    assert content.loanword[0].loanword == "örnek yabancı sözcük"
    assert content.trending_words[0].word == "örnek madde"
    assert content.trending_words[0].type == "gunun_kelimesi"
