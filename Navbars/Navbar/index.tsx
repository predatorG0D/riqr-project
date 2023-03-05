import { ButtonGroup, Button, Container } from "react-bootstrap"
import styles from './style.module.scss'
import exitIcon from '../../../public/icons/exite.svg'
import Link from 'next/link'
import { Logo } from "../../Logo"
import { useModalContext } from "../../../contexts/modals"
import { logoutReq } from "../../../api/auth"
import { AUTH } from "../../../constants/modal"
import { useDispatch, useSelector } from "react-redux"
import { logout } from "../../../redux/actions/auth"


const routers = [
    { title: "Как это работает?", url: "/info/how-it-works" },
    { title: "Контакты", url: "/info/contacts" }
]

export const Navbar = () => {
    const modal = useModalContext();
    const dispatch = useDispatch();
    const isLoggedIn = useSelector((state:any) => state.auth.isLoggedIn);
    const handleOpen = () => modal?.setModal({name: AUTH, isShow: true, tabId: 'auth'});
    const handleLogout = () => dispatch(logout());
    
    return (
        <header className={styles.navbar}>
            <Container className={styles.navbar_content}>
                <Logo/>
                <div className={styles.navbar_items}>
                    {routers.map((val, ind) => {
                        return (
                            <Link key={ind} href={val.url}>{val.title}</Link>
                        )
                    })}
                </div>
                {isLoggedIn? (
                    <ButtonGroup className={styles.btn_group}>
                        <Button variant="outline-light">
                            <Link href="/cabinet">
                                <p className={styles.link}>Личный кабинет</p>
                            </Link>
                        </Button>
                        <Button variant="outline-light" onClick={handleLogout}><img src={exitIcon.src} /></Button>
                    </ButtonGroup>
                ):<Button className={styles.link} variant="outline-light" onClick={handleOpen}>Вход</Button>}
                
            </Container>
        </header>
    )
}

