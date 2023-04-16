import React, { useState } from "react";
import { War } from "../../../../models/war";
import styles from "./WarInSubmission.module.scss";
import { WarInSubmissionMeme } from "./meme/WarInSubmissionMeme";
import { useWarMemes } from "../../../../hooks/useWarMemes";
import { Loader } from "../../../components/loader/Loader";
import { WarHeader } from "../../../components/war-header/WarHeader";
import { memeService } from "../../../../services/memeService";

interface WarInSubmissionProps {
  war: War;
}

export function WarInSubmission({ war }: WarInSubmissionProps) {
  const { memes, setMemes, isLoading, setIsLoading } = useWarMemes(war.id);

  async function uploadMeme(event: any): Promise<void> {
    setIsLoading(true);
    const meme = await memeService.uploadMeme(war.id, event.target.files[0]);
    setMemes([ meme, ...memes ]);
    setIsLoading(false);
  }

  async function deleteMeme(memeID: number): Promise<void> {
    await memeService.deleteMeme(memeID);
    setMemes(memes.filter(meme => meme.id != memeID));
  }

  if (isLoading) return <Loader/>;

  return (
    <>
      <WarHeader war={ war }>
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
      </WarHeader>
      <form className={ styles.uploadedMemesForm }>
        <label htmlFor="file-upload" className={ styles.uploadFileButton }>
          <input id="file-upload" type="file" onChange={ uploadMeme }/>
          Upload new meme
        </label>
        { memes.map(meme => (
          <WarInSubmissionMeme
            key={ meme.id }
            meme={ meme }
            displayApprovalStatus={ war.requires_meme_approval }
            onDelete={ () => deleteMeme(meme.id) }
          />
        )) }
      </form>
    </>
  );
}
