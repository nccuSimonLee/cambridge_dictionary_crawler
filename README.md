# Observations

## 範例網頁

[https://dictionary.cambridge.org/dictionary/english-chinese-traditional/back](https://dictionary.cambridge.org/dictionary/english-chinese-traditional/back)

[https://dictionary.cambridge.org/dictionary/english-chinese-traditional/baby-blues](https://dictionary.cambridge.org/dictionary/english-chinese-traditional/baby-blues)

[https://dictionary.cambridge.org/dictionary/english-chinese-traditional/bank](https://dictionary.cambridge.org/dictionary/english-chinese-traditional/bank)

## Thoughts

### Hypothesis

目前看來單字網頁的組成形式應該是

- POS block
    - big sense block
        - sense block
            - example sentences
        - phrase block (if exists)
        - extra example sentences

需要注意的是，[一個 POS block 可能會有多個 POS tags](https://dictionary.cambridge.org/dictionary/english-chinese-traditional/inside)。

而可能也會有[多個 pos block 對應到同一個 pos tag](https://dictionary.cambridge.org/dictionary/english-chinese-traditional/miss)。

### Working logic

爬取一個網頁資料的流程如下：

1. 抓出所有的 pos blocks
2. 針對一個 pos block 做處理，抓出 big sense blocks
3. 對每個 big sense blocks 抽出 guide word (if exists) 並執行 step 4. ~ 6.
4. 抓出 sense blocks，並從中抽出：
    - en_def
    - ch_def
    - level (if exists)
    - example sentences
5. 抓出 extra example sentences
6. 抓出 phrase blocks (if exists)，抽出資料的作法類似於 sense blocks
7. 回到第二步，直到所有 pos blocks 都被處理過

### Proposed works
對上述的每種 block 設計一個 class，負責執行上面提到的工作。除了最底層的 block (sense block and phrase block) 以外，都要抓出某些更底層的 block。而如果將抽取資料以及更底層 block 的動作放在 instantiation 中的話，就會產生上面 working logic 的效果。 最頂層的 class 就是 page of vocabulary。它擁有自己的一些資料，以及 POS blocks。而每個 POS block 也同樣地擁有自己的資料以及 big sense blocks，以此類推。舉例來說，當 instantiate bank 這個詞的 vocabulary page 的時候，它就會 instantiate POS blocks，而在 instantiate 每個 POS blocks 的時候，它們又會去 instantiate big sense blocks，以此類推。從而產生類似 for loop 的效果，但我們又能夠分別對各個 class 進行設計，提高了可維護性。

# 用來代表一個 vocab page 的 classes

## VocabPage

- vocab
- POS blocks

## POSBlock

- headword
- pos tag : `list`
- big sense blocks

## BigSenseBlock

- guide word
- sense blocks
- phrase blocks
- extra examples

## SenseBlock

- English definition
- Chinese definition
- example sentences，為一個 `list`，其中每個元素為 `dict` 包含：
    - English version
    - Chinese version
- level
- gcs

## PhraseBlock

- term
- level
- sense list，其中的每個元素都是一個 sense 包含：
    - English definition
    - Chinese definition
    - example sentences