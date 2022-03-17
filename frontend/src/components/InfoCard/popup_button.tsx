import { Button, Modal, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, useDisclosure } from "@chakra-ui/react"

export interface PopupProps {
  title: string,
  subtitle?: string,
  content?: any,
}

/**
 * @returns PopUp Button, when clicked, brings up a modal
 */
function PopUpButton(props: PopupProps) {
  const { isOpen, onOpen, onClose } = useDisclosure()

  return (
    <>
      <Button onClick={onOpen}>Trigger modal</Button>

      <Modal onClose={onClose} isOpen={isOpen} isCentered>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>{props.title}</ModalHeader>
          <ModalBody>{props.content}</ModalBody>
        </ModalContent>
      </Modal>
    </>
  )
}

export default PopUpButton