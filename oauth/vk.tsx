import { NextPage, NextPageContext } from "next";
import { useRouter } from "next/router";
import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { entryVk } from "../../redux/actions/auth";



const Vk: NextPage = ({code}: any) => {
    const dispatch = useDispatch();
    useEffect(()=> {
        dispatch(entryVk(code));
    }, [])
    return (
        <div>

        </div>
    );
}
Vk.getInitialProps = async (ctx: NextPageContext) => {
    return { code: ctx.query.code }
}
export default Vk