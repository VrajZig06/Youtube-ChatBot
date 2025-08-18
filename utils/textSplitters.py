from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_text(dataList:list,sizeOfChunk:int = 500):

    try:
        transcripts = [data.text for data in dataList]
        texts = " ".join(transcripts)

        # Create recursive text splitters 
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = sizeOfChunk,
            chunk_overlap = 100
        )

        # Split Text into 100 Character Size Chunks 
        chunksList = splitter.split_text(texts)

        return chunksList

    except Exception as e:
        print(f"Error : {e}")