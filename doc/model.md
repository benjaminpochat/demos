# Domain model

Ubiquitous language :
- Local government
- Official council meeting report
- Deliberation
- Web document
- Text document

```
-- web scraping domain ------------------------------|
|                                                    |
|  | Local gov     | 1       n | Resource       |    |
|  _________________<----------__________________    |
|  | Name          |           | Id [(SHA1(url)]|    |
|  | Domain        |           | Url            |    |
|  |               |           | Language       |    |
|  _________________           | Resource type  |    |
|                              __________________    |
|____________________________________________________|
                         



-- document to text conversion domain -----------------------|    
|                                                            |    
|  | Document         |            | Resource         |      |    
|  ____________________            ____________________      |    
|  | Id               |            | Id               |      |    
|  | Raw content      |            | Url              |      |    
|  | Text content     |            | Language         |      |    
|  | Conversion error |            |                  |      |    
|  ____________________            ____________________      |    
|____________________________________________________________|                                 




-- document classification -|
|                           |
|  | Document      |        |
|  _________________        |
|  | Id            |        |
|  | Text content  |        |
|  | Document class|        |
|  _________________        |
|___________________________|


```
