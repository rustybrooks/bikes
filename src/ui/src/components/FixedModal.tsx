import { Modal, ModalProps } from '@mantine/core';

export const FixedModal = (props: ModalProps) => {
  return (
    <>
      <Modal.Root opened={props.opened} onClose={props.onClose} size={props.size}>
        {props.withOverlay ? <Modal.Overlay /> : null}
        <Modal.Content style={{ left: 0, right: 0 }}>
          <Modal.Header>
            <Modal.Title>{props.title}</Modal.Title>
            {props.withCloseButton ? <Modal.CloseButton /> : null}
          </Modal.Header>
          <Modal.Body>{props.children}</Modal.Body>
        </Modal.Content>
      </Modal.Root>
    </>
  );
};
