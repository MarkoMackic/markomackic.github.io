if [ -n "$1" ] && [ -n "$2" ]; then
sed -i "s/$1/$2/g" build_dsn_assets.sh;
ls _posts/ | grep decentralized-git-social-network | xargs -I{} sed -i "s/$1/$2/g" _posts/{};
exit;
fi

echo "Params not supplied";
exit 1;

