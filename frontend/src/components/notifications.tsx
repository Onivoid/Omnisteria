import { Toast } from 'primereact/toast'
import { useEffect, useRef } from 'react'


export function notify(toast: React.MutableRefObject<Toast | null>, message: string, type: string) {
  if(!toast.current) return
  if(type === 'success') {
    toast.current.show({severity: 'success', summary: 'Success', detail: message})
  } else if(type === 'error') {
    toast.current.show({severity: 'error', summary: 'Error', detail: message})
  } else if(type === 'warning') {
    toast.current.show({severity: 'warn', summary: 'Warning', detail: message})
  }
}

export function Notifications({message, type}:{message: string, type: string}) {
  const toast = useRef<Toast>(null)

  useEffect(() => {
    notify(toast, message, type)
  }, [message, type])

  return (
    <Toast ref={toast} />
  )
}