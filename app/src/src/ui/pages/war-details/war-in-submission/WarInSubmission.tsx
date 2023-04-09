import React, { useState } from "react";
import { War } from "../../../../models/war";
import styles from "./WarInSubmission.module.scss";
import { WarInSubmissionMeme } from "./meme/WarInSubmissionMeme";

interface WarInSubmissionProps {
  war: War;
}

export function WarInSubmission({ war }: WarInSubmissionProps) {
  const [ newImages, setNewImages ] = useState<File[]>([]);
  // TODO: init existing images (useEffect)
  // TODO: init deleted images

  function onImageUpload(event: any): void {
    setNewImages([ event.target.files[0], ...newImages ]);
  }

  return (
    <form className={ styles.uploadedMemesForm }>
      <label htmlFor="file-upload" className={ styles.uploadFileButton }>
        <input id="file-upload" type="file" onChange={ onImageUpload }/>
        Upload new meme
      </label>
      { newImages.map(file => <WarInSubmissionMeme key={ file.name } file={ file }/>) }
    </form>
  );
}
