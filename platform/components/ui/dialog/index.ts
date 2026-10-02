import { Dialog as DialogPrimitive } from 'bits-ui';
import Content from './dialog-content.svelte';
import Description from './dialog-description.svelte';
import Overlay from './dialog-overlay.svelte';
import Portal from './dialog-portal.svelte';
import Title from './dialog-title.svelte';
import Root from './dialog.svelte';

const Trigger = DialogPrimitive.Trigger;
const Close = DialogPrimitive.Close;

export {
	Root,
	Trigger,
	Close,
	Portal,
	Overlay,
	Content,
	Title,
	Description,
	//
	Root as Dialog,
	Trigger as DialogTrigger,
	Close as DialogClose,
	Portal as DialogPortal,
	Overlay as DialogOverlay,
	Content as DialogContent,
	Title as DialogTitle,
	Description as DialogDescription
};
