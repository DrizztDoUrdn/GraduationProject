# Ise yariyor
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

tokenizer = AutoTokenizer.from_pretrained("mdeniz1/turkish-sentiment-analysis-bert-base-turkish-uncased")
model = AutoModelForSequenceClassification.from_pretrained("mdeniz1/turkish-sentiment-analysis-bert-base-turkish"
                                                           "-uncased", from_tf=True)

pipe = pipeline("text-classification", model="mdeniz1/turkish-sentiment-analysis-bert-base-turkish-uncased")

p = pipe("makinede sorun yok gayet iyi kahve yapıyor amazon ürünü ai̇t kurye firma gönderiyor dikkat edin kargo değil kurye siparişten 2 gün 1 saat teslim edilecek mesaj geldi hemen 2 dakika geldik bulamadık iade işlemi başladı mesajı geldi kuryenin telefonu vardı aradım elemanı abi paket büyük getiremem başkası getirsin yüzden iade girdim dedi bunlar yapıyormuş i̇nternet'ten ai̇t kuryeyi aratın milyon tane şikayet sağdan soldan işsiz kalmış motorculara paket taşıtıyorlar getiren eleman ai̇t çalışanı olmadığını söyle")
print(p)
# [{'label': 'LABEL_1', 'score': 0.9871089}]
# LABEL_2 Positive
# LABEL_1 Neutral
# Label_0 Negative
print(p[0]['label'] == 'LABEL_2')

