import React, { useState } from "react";
import { War } from "../../../../models/War";
import styles from "./WarInSubmission.module.scss";
import { WarInSubmissionMeme } from "./meme/WarInSubmissionMeme";
import { useWarMemes } from "../../../../hooks/useWarMemes";
import { Loader } from "../../../components/loader/Loader";
import { WarHeader } from "../../../components/war-header/WarHeader";
import { memeService } from "../../../../services/memeService";
import { Modal } from "../../../components/modal/Modal";

interface WarInSubmissionProps {
  war: War;
}

export function WarInSubmission({ war }: WarInSubmissionProps) {
  const { memes, setMemes, isLoading, setIsLoading } = useWarMemes(war.id, 20);
  const [ errorMessages, setErrorMessages ] = useState<string[]>([]);
  const [ hasOpenedErrorModal, setHasOpenedErrorModal ] = useState<boolean>(false);

  async function uploadMeme(event: any): Promise<void> {
    setIsLoading(true);
    try {
      const meme = await memeService.uploadMeme(war.id, event.target.files[0]);
      setMemes([ meme, ...memes ]);
    } catch (error: any) {
      if (error.response.data.code === "meme_upload_limit_reached") {
        setErrorMessages([
          "You uploaded enough memes already!",
          "Take a break or something....",
          "If you really want to upload that meme, you're gonna have to delete " +
          "one of the uploaded once to make a rome for a new one.",
          "I'm sure you uploaded a couple of unworthy memes that can easily be trashed 🤭",
        ]);
      } else {
        setErrorMessages([ "Something went wrong 😬" ]);
      }
      setHasOpenedErrorModal(true);
    }
    setIsLoading(false);
  }

  async function deleteMeme(memeID: number): Promise<void> {
    try {
      await memeService.deleteMeme(memeID);
      setMemes(memes.filter(meme => meme.id != memeID));
    } catch (error) {
      setErrorMessages([ "Something went wrong 😬" ]);
      setHasOpenedErrorModal(true);
    }
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
      { errorMessages && (
        <Modal isOpened={ hasOpenedErrorModal } onClose={ () => setHasOpenedErrorModal(false) }>
          <div className={ styles.errorMessages }>
            { errorMessages.map((errorMessage, index) => <p key={ index }>{ errorMessage }</p>) }
          </div>
        </Modal>
      ) }
    </>
  );
}
