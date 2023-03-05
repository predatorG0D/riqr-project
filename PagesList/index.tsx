import { Button, Image } from "react-bootstrap"
import { useState } from "react"
import csx from "classnames"
import styles from './style.module.scss'
import { ModalDelete } from "../Modals/ModalDelete"
import { useRouter } from "next/router"
import { pathFromServer } from "../../utils/fromServer"
import { useModalContext } from "../../contexts/modals"
import { DELETE, PAY } from "../../constants/modal"

interface PagesList {
    pages: Array<any>
}

export const PagesList = ({pages}: PagesList) => {
    return (
        <>
            <ModalDelete/>
            {pages.map((page, ind)=> {
                return !page.error? <Page {...page} key={page.id}/>: null
            })}
        </>
    )
}

interface PageProps {
    status: number,
    name: string,
    surname: string,
    price: number,
    payed: boolean,
    private: boolean,
    time_left: number,
    id: number,
    avatar: string
}


export const Page = ({
    status,
    name,
    surname,
    price,
    payed,
    private: priv,
    time_left,
    avatar,
    id
} : PageProps) => {
    const modal = useModalContext();
    const router = useRouter();
    
    const handleDelete = () => modal?.setModal({name: DELETE, isShow: true, pageIdDelete: id})
    const handleOpenPay = () => modal?.setModal({name: PAY, isShow: true})
    const handleShowPage = () => router.push(`/page/${id}`)
    const handleEdit = () => router.push(`/cabinet/update/${id}`)

    const statusActiveItems = (status: number) => {
        if(!payed) return (
            <div className={styles.status_content__buttons}>
                <Button className={styles.button} onClick={handleOpenPay}>Оплатить</Button>
                <div className={styles.price}>{price}₽</div>
            </div>
        )
        if(payed) return (
            <div className={styles.hidden_page}>
                <div>Скрыть страницу</div>
                <div className={styles.checkbox}>
                    <input className={styles.checkbox_field} type="checkbox" defaultChecked={priv}/>
                    <span></span>
                </div>
                
            </div>
        ) 
    }

    const statusPage = (status: number) => {
        if(!payed && time_left > 0) return (
            <div className={styles.status_content}>
                <p>Осталось {time_left} дня пробного периода</p>
            </div>
        )
        else if(time_left <= 0) return (
            <div className={styles.status_content}>
                <p>Пробный период истёк</p>
            </div>
        )
    }

    return (
        <div className={styles.block}>
            <div className={styles.fio} onClick={handleShowPage} tabIndex={0}>
                <Image src={pathFromServer(avatar)} roundedCircle width="50px" height="50px"/>
                <div>
                    <p>{name}</p>
                    <p>{surname}</p>
                </div>
            </div>
            {statusPage(status)}
            {statusActiveItems(status)}
            <div className={csx(styles.buttons)}>
                <Button 
                    className={styles.btn}
                    variant="outline-primary" 
                    onClick={handleEdit}>Изменить</Button>
                <Button 
                    className={styles.btn}
                    variant="outline-danger"
                    onClick={handleDelete}>Удалить</Button>
            
            </div>
        </div>
    )
}

