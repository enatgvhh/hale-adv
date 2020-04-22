#

INSPIRE Transformation der AdV-Daten mit HALE Studio
====================================================

## Inhalt
* [Einleitung](#einleitung)
* [HALE Transformation AdV INSPIRE alignments](#hale-transformation-adv-inspire-alignments)
* [GML-Loader deegree-gml-tool](#gml-loader-deegree-gml-tool)
* [FME Data Pipeline](#fme-data-pipeline)
* [Summary](#summary)


## Einleitung
Bedauerlicherweise habe ich nun auch die Transformation und Bereitstellung der AdV-Daten für INSPIRE geerbt. Die [AdV]( http://www.adv-online.de/Startseite/) hat für Deutschland das einheitliche AAA-Modell etabliert und natürlich sind die ALKIS und ATKIS Daten von so immenser Wichtigkeit, dass sie zusätzlich auch im INSPIRE Zielmodell bereitgestellt werden müssen. Ja, es wurde sogar eine eigene Spezifikation auf die INSPIRE-Spezifikation draufgesetzt. Der Irrsinn kennt keine Grenzen. Zumindest hat die AdV dazu von der Firma wetransform die entsprechenden Transformationsmodelle entwickeln lassen, die in HALE Studio bzw. HALE Connect zum Einsatz kommen.

Auch bei uns wird HALE Studio mit den AdV INSPIRE alignments seit mehreren Jahren eingesetzt. Es fehlte nur ein flüssiger Workflow mit Automatisierung. Der Workflow besteht aus den folgenden Schritten.

* NAS-Files mit HALE Studio in INSPIRE GML-Files transformieren
* Datenbanktabellen leeren
* INSPIRE GML-Files mit dem GML-Loader (deegree-gml-tool) in einen deegree SQLFeatureStore laden
* Datenbanktabellen warten
* FME Pipeline in die produktive Datenbank

Zur Automatisierung habe ich das kleine python-package 'adv' entwickelt, welches zusammen mit einem Client im Ordner [src](src) zu finden ist. 


## HALE Transformation AdV INSPIRE alignments
Für die Transformation benötigen wir [HALE Studio](https://www.wetransform.to/products/halestudio/), das wir uns als [Snapshot](https://builds.wetransform.to/job/hale/job/hale~publish(master)/) herunterladen. Zusätzlich benötigen wir das gradle Projekt mit den AdV INSPIRE alignments. Ansprechpartner hierfür ist die AdV. Dann downloaden wir uns [gradle](https://gradle.org/releases/) in der benötigten Version und kopieren den Inhalt nach *C:\Gradle\gradle-version*, setzen *GRADLE_HOME* sowie *PATH* und sind startklar.
```
GRADLE_HOME: C:\Gradle\gradle-4.8
Path: %GRADLE_HOME%\bin

gradle -v

cd C:\...\inspire_alignements
gradle tasks -all
gradle transform-au-dlkm-kommunalesGebiet
```
Im python-package 'adv' werden die gradle-tasks über ein Objekt der Klasse *GradleProcess* gestartet. Alle Tasks für ein Projekt werden in einem Objekt der Klasse *ConfigProject* gespeichert, welches seinen Input aus einem member-Element des [Konfigurations-Files]( src/ConfigAdv.xml) bezieht. Die bei der Transformation erzeugten GML-Files werden im gradle Projekt in den Unterordner *transformiert* geschrieben.


## GML-Loader deegree-gml-tool
Über ein Objekt der Klasse *PostgreProcess* erfolgen das Leeren sowie die Wartung der Datenbanktabellen, die ebenfalls im Konfigurationsfile definiert werden. Dazwischen setzen wir den GML-Loader (*deegree-gml-tool-1.1.jar*) zum Laden der INSPIRE GML-Files in die Datenbank ein. Die vollständigen Java-Kommandos sind im Konfigurationsfile anzugeben. Gestartet werden sie über ein Objekt der Klasse *JavaProcess*. Der GML-Loader funktioniert in der eingesetzten Version ausgezeichnet. Ich kann also die negativen Bewertungen zu früheren Versionen widerlegen.


## FME Data Pipeline
Sowohl HALE Studio als auch der deegree GML-Loader sind große Ressourcenfresser. Wir setzen sie deshalb nur auf einer Stage-Umgebung ein. Den Transfer der Daten in die produktive Datenbank bewerkstelligen wir mit FME. Je Projekt gibt es dazu eine FME Workbench, die über ein Objekt der Klasse *FmeProcess* gestartet und im Konfigurationsfile definiert wird.

FME ist ein ausgereiftes Werkzeug, mit dem ich ansonsten alle [INSPIRE-Transformationen]( https://github.com/enatgvhh/inspire) umgesetzt habe. HALE ist dazu keine Konkurrenz.


## Summary
Persönlich würde ich FME immer HALE vorziehen. Anderseits ist es natürlich mit sehr viel Aufwand verbunden, neue 'aaa2inspire' Transformationsmodelle in FME zu erstellen und diese den Versionsänderungen anzupassen. HALE spart hier also Zeit und Energie. Das hat aber seinen Preis. Viele Transformationsergebnisse finde ich qualitativ absolut nicht überzeugend,vom Workflow sowie der Notwendigkeit eigene Transformer völlig neu zu programmieren, ganz zu schweigen. 
