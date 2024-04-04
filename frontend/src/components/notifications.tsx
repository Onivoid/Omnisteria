import { Toast } from 'primereact/toast'
import { useEffect, useRef } from 'react'


export function notify(toast: React.MutableRefObject<Toast | null>, message: string, type: string) {
  if(!toast.current) return
  if(type === 'success') {
    toast.current.show({severity: 'success', detail: message})
  } else if(type === 'error') {
    toast.current.show({severity: 'error', detail: message})
  } else if(type === 'warning') {
    toast.current.show({severity: 'warn', detail: message})
  }
}

export function Notifications({notifications}:{notifications: {message: string, type: string}[]}) {
  const toast = useRef<Toast>(null)

  useEffect(() => {
    notifications.forEach((notification, index) => {
      notify(toast, notification.message, notification.type)
    })
  }, [notifications])

  return (
    <Toast ref={toast} />
  )
}