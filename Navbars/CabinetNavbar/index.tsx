import classNames from "classnames"
import { useRouter } from "next/dist/client/router"
import { Button, Container } from "react-bootstrap"
import exitIcon from '../../../public/icons/exite.svg'
import styles from './style.module.scss'
import Link from 'next/link'
import { Logo } from "../../Logo"
import { useDispatch } from "react-redux"
import { logout } from "../../../redux/actions/auth"
import { useEffect } from "react"
import { useModalContext } from "../../../contexts/modals"

const pages = [
    { title: "Мой аккаунт", pathname: '/cabinet' },
    { title: "Создать страницу", pathname: '/cabinet/create' },
    { title: "Мои страницы", pathname: '/cabinet/pages' },
    { title: "Техподдержка", pathname: '/cabinet/supporting' }
]

const routers = [
    { title: "Как это работает?", url: "/info/how-it-works" },
    { title: "Контакты", url: "/info/contacts" }
]

export const CabinetNavbar = () => {
    const router = useRouter();
    const modal = useModalContext();
    const dispatch = useDispatch();
    const handleClick = (path: string) => router.push(path)
    const handleLogout = () => {
        dispatch(logout());
        router.push('/');
    };
    
    useEffect(()=>{
        modal?.setModal({...modal.state,isShow: false});
    }, [])

    return (
        <div>
            <div className={styles.navbar}>
                <Container className={styles.navbar_content}>
                    <Logo/>
                    <div className={styles.navbar_items}>
                        {routers.map((val, ind) => {
                            return (
                                <Link key={ind} href={val.url}>{val.title}</Link>
                            )
                        })}
                    </div>
                    <Button variant="outline-light" onClick={handleLogout}><img src={exitIcon.src} /></Button>
                </Container>
            </div>
            <div className={styles.cabinet_navbar}>
                <ul className={styles.items}>
                    {pages.map((val, ind)=> {
                        return (
                            <li key={ind} 
                                onClick={()=> handleClick(val.pathname)} 
                                className={
                                    classNames({[styles.active]: val.pathname == router.pathname})
                                }>{val.title}</li>
                        )
                    })}
                </ul>
            </div>
        </div>
    )
}