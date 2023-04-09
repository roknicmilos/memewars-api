import React, { useEffect, useState } from "react";
import styles from "./WarInSubmissionMeme.module.scss";
import { fileService } from "../../../../../services/fileService";

interface WarInSubmissionMemeProps {
  file: File;

  onImageRemove?(): void;
}

export function WarInSubmissionMeme({ file }: WarInSubmissionMemeProps) {
  const [ base64image, setBase64image ] = useState<string>("");

  useEffect(() => {
    fileService.file2Base64(file).then(base64value => setBase64image(base64value));
  }, []);

  return (
    <div className={ styles.meme }>
      <img
        className={ styles.memeImage }
        src={ base64image }
        alt={ file.name }
      />
    </div>
  );
}
