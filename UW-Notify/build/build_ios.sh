IPA=$(ls -t ../*.ipa 2>/dev/null | head -n1); echo "$IPA"

eas build --local --profile production --platform ios \
&& eas submit -p ios --path "$IPA"

