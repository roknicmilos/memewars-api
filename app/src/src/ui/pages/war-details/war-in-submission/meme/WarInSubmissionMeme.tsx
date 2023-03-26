import React, { useState } from "react";
import styles from "./WarInSubmissionMeme.module.scss";
import { Modal } from "../../../../components/modal/Modal";

interface WarInSubmissionMemeProps {
  image: any;
  index: number;

  onImageRemove(): void;
}

export function WarInSubmissionMeme({ image, index, onImageRemove }: WarInSubmissionMemeProps) {
  const [ hasOpenedOptions, setHasOpenedOptions ] = useState<boolean>(false);

  console.log(image);

  return (
    <div key={ index } className={ styles.meme }>
      <img
        className={ styles.memeImage }
        src={ image.dataURL }
        alt={ image.name }
        onClick={ () => setHasOpenedOptions(true) }
      />
      <Modal isOpened={ hasOpenedOptions } onClose={ () => setHasOpenedOptions(false) }>
        <div className={ styles.fileModalInfo }>
          <p>
            <span className={ styles.label }>File name:</span> { image.file.name }
          </p>
          <p>
            <span className={ styles.label }>File size:</span> { (image.file.size / 1000).toFixed(2) } KB
          </p>
        </div>
        <div className={ styles.deleteButton } onClick={ () => alert("deleeete") }>Delete meme</div>
      </Modal>
    </div>
  );
}
