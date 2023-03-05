import moment from "moment"
import { Col, Row } from "react-bootstrap"
import { pathFromServer } from "../../../utils/fromServer"
import styles from './style.module.scss'
require('moment/locale/ru')

interface BiographyProps {
    user: any
}

export const Biography = ({user}: BiographyProps) => {
    moment.locale('ru')
    const haveAvatar = user.avatar?.url? true : false;
    return (
        <Row md={haveAvatar? 2: 1} xs={1} className={styles.row}>
            {
            haveAvatar? (
                <>
                    <Col>
                        <div className={styles.fio}>
                            <h1>{user.name}</h1>
                            <h1>{user.surname}</h1>
                            <h1>{user.otchestvo}</h1>
                        </div>
                        <table className={styles.biography}>
                            <tr>
                                <td>Место рождения:</td>
                                <td>{user.place_of_birth}</td>
                            </tr>
                            <tr>
                                <td>дата: </td>
                                <td>{moment(user.date_of_birth).format('LL')}</td>
                            </tr>
                            <tr>
                                <td>Место смерти: </td>
                                <td>{user.place_of_death}</td>
                            </tr>
                            <tr>
                                <td>дата: </td>
                                <td>{moment(user.date_of_death).format('LL')}</td>
                            </tr>
                            <tr>
                                <td>Национальность: </td>
                                <td className={styles.nationaly}>
                                    <img className={styles.flag} src={pathFromServer(user.nationality.icon)}/>
                                    <p> {user.nationality.name}</p> 
                                </td>
                            </tr>
                        </table>
                        {/* <div className={styles.biography}>
                            <div className={styles.biography_placeholder}>
                                <div>
                                    <p className={styles.info_text}>Место рождения: </p>
                                    <p className={styles.info_text}>дата: </p>
                                </div>
                                <div>
                                    <p className={styles.info_text}>Место смерти: </p>
                                    <p className={styles.info_text}>дата: </p>
                                </div>
                                <div>
                                    <p className={styles.info_text}>Национальность: </p>
                                </div>
                            </div>
                            <div className={styles.biography_data}>
                                <div >
                                    <p>{user.place_of_birth}</p>
                                    <p>{moment(user.date_of_birth).format('LL')}</p> 
                                </div>
                                <div>
                                    <p>{user.place_of_death}</p>
                                    <p>{moment(user.date_of_death).format('LL')}</p> 
                                </div>
                                <div className={styles.nationaly}>
                                    <img className={styles.flag} src={pathFromServer(user.nationality.icon)}/>
                                    <p> {user.nationality.name}</p> 
                                </div>
                            </div>
                        </div> */}
                    </Col>
                    <Col className={styles.col_image}>
                        <img src={pathFromServer(user.avatar.url)} className={styles.main_image}/>
                    </Col>
                </>
            ): (
                <Col>
                    <div className={styles.fio}>
                        <h1>{user.name}</h1>
                        <h1>{user.surname}</h1>
                        <h1>{user.otchestvo}</h1>
                    </div>
                    <div className={styles.biography}>
                        <div className={styles.biography_placeholder}>
                            <div>
                                <p className={styles.info_text}>Место рождения: </p>
                                <p className={styles.info_text}>дата: </p>
                            </div>
                            <div>
                                <p className={styles.info_text}>Место смерти: </p>
                                <p className={styles.info_text}>дата: </p>
                            </div>
                            <div>
                                <p className={styles.info_text}>Национальность: </p>
                            </div>
                        </div>
                        <div className={styles.biography_data}>
                            <div >
                                <p>{user.place_of_birth}</p>
                                <p>{moment(user.date_of_birth).format('LL')}</p> 
                            </div>
                            <div>
                                <p>{user.place_of_death}</p>
                                <p>{moment(user.date_of_death).format('LL')}</p> 
                            </div>
                            <div className={styles.nationaly}>
                                <img className={styles.flag} src={pathFromServer(user.nationality.icon)}/>
                                <p> {user.nationality.name}</p> 
                            </div>
                        </div>
                    </div>
                </Col>
                ) 
            }
            
        </Row>
    )
}