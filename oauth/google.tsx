import { NextPage, NextPageContext } from "next";
import { useRouter } from "next/router";
import { useEffect } from "react";
import { useDispatch } from "react-redux";
import { entryGoogle } from "../../redux/actions/auth";



const Google: NextPage = ({code}: any) => {
    const dispatch = useDispatch();
    useEffect(()=> {
        dispatch(entryGoogle(code));
    }, [])
    return (
        <div>

        </div>
    );
}
Google.getInitialProps = async (ctx: NextPageContext) => {
    if(ctx.query.error) {
        return {
            
        }
    }
    return { code: ctx.query.code }
}
export default Google