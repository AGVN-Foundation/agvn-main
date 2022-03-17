import React from 'react';
import Cookies from 'universal-cookie';
import { useRouter } from 'next/router';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import { nominalTypeHack } from 'prop-types';

const host = "http://127.0.0.1:8000/api/v1";

interface PopupsProps {
  type: string;
  message?: string;
  toSignin?: boolean;
  toEdit?: boolean;
}

export default function Popups ({ type, message, toSignin, toEdit}: PopupsProps) {
  const [show, setShow] = React.useState(false);
  const router = useRouter();
  const cookies = new Cookies();

  React.useEffect(() => {
    if (type === "error" || type=== "success") {
      setShow(!!message);
    }
  }, [type, message]);

  function makeInvisible () {
    setShow(false);
    if (toSignin === true) {
      toSigninPage();
    } else if (toEdit === true) {
      toEditPage();
    }
  }
  
  function toSigninPage () {
    cookies.remove('token');
    router.push('/signin');
  }

  function toEditPage () {
    router.push('/profile/edit')
  }

  return (
    <>
      {type === 'error' && (
        <div>
          <Modal show={show} onHide={makeInvisible}>
            <Modal.Header aria-label="close-button" closeButton>
              <Modal.Title>Error!</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              {message}
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={makeInvisible}>Dismiss</Button>
            </Modal.Footer>
          </Modal>
        </div>
      )}
      {type === 'success' && (
        <div>
          <Modal show={show} onHide={makeInvisible}>
            <Modal.Header aria-label="close-button" closeButton>
              <Modal.Title>Success!</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              {message}
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={makeInvisible}>Continue</Button>
            </Modal.Footer>
          </Modal>
        </div>
      )}
    </>
  )
}
