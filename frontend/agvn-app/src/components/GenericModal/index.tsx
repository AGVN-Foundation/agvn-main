import React, { useState } from "react";
import { Button, Modal } from "react-bootstrap";

export interface GenericModalProps {
  title: string
  buttonText: string
  content?: any
  closeButton?: boolean
  footer?: boolean
}

function GenericModal(props: GenericModalProps) {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  return (
    <>
      <Button variant="primary" onClick={handleShow}>
        {props.buttonText}
      </Button>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>{props.title}</Modal.Title>
        </Modal.Header>
        <Modal.Body>{props.content}</Modal.Body>
      </Modal>
    </>
  );
}

export default GenericModal
