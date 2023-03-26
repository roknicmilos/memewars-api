import React from "react";
import { War } from "../../../../models/war";
import styles from "./WarInSubmission.module.scss";
import ImageUploading, { ImageListType } from "react-images-uploading";
import { WarInSubmissionMeme } from "./meme/WarInSubmissionMeme";

interface WarInSubmissionProps {
  war: War;
}

export function WarInSubmission({ war }: WarInSubmissionProps) {

  const [ images, setImages ] = React.useState<ImageListType>([]);

  function onMemeUploadChange(imageList: ImageListType, addUpdateIndex?: Array<number>) {
    setImages(imageList);
  }

  return (
      <ImageUploading
        multiple
        value={ images }
        onChange={ onMemeUploadChange }
        maxNumber={ 12 }
        dataURLKey="dataURL"
      >
        { ({ imageList, onImageUpload, onImageRemove }) => (
          <div className={styles.uploadedMemes}>
            <button onClick={ onImageUpload }>
              Upload a new meme
            </button>
            { imageList.map((image, index) => (
              <WarInSubmissionMeme image={ image } index={ index } onImageRemove={ () => onImageRemove(index) }/>
            )) }
          </div>
        ) }
      </ImageUploading>
  );
}
