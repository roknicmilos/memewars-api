import React, { useState } from "react";
import { War } from "../../../../models/war";
import styles from "./WarInSubmission.module.scss";
import { WarInSubmissionMeme } from "./meme/WarInSubmissionMeme";
import { useWarMemes } from "../../../../hooks/useWarMemes";
import { Loader } from "../../../components/loader/Loader";
import { WarHeader } from "../../../components/war-header/WarHeader";

interface WarInSubmissionProps {
  war: War;
}

export function WarInSubmission({ war }: WarInSubmissionProps) {
  const [ memes, isLoading ] = useWarMemes(war.id);
  const [ hasOpenedHeader, setHasOpenedHeader ] = useState<boolean>(false);

  function onImageUpload(event: any): void {
    alert("TODO: request to API to create the meme");
  }

  function toggleHeader() {
    setHasOpenedHeader(!hasOpenedHeader);
  }

  if (isLoading) return <Loader/>;

  return (
    <>
      <WarHeader
        war={ war }
        isOpened={ hasOpenedHeader }
        onClick={ toggleHeader }
      />
      <div className={ styles.explanatoryText }>
        <p>
          Upload or remove memes that are going to be a part
          of <span className={ styles.boldText }>{ war.name }</span>.
        </p>
        { war.requires_meme_approval && (
          <p>
            Because this war requires approval of all memes, only the approved
            memes that you uploaded will end up in the next phase of the war.
          </p>
        ) }
      </div>
      <form className={ styles.uploadedMemesForm }>
        <label htmlFor="file-upload" className={ styles.uploadFileButton }>
          <input id="file-upload" type="file" onChange={ onImageUpload }/>
          Upload new meme
        </label>
        { memes.map(meme => <WarInSubmissionMeme key={ meme.id } meme={ meme }/>) }
      </form>
    </>
  );
}
